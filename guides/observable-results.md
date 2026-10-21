# 可观察结果：怎样知道实验真的通过

[项目首页](../README.md) · [逐节点实验](../nodes/README.md)

每次实验先写预测，再运行；先完成确定性的输出检查，再判断生成内容。卡片中的结果都是**待验证预期**，不是已有实测报告。

## 1. 固定基准，单独改一个变量

记录 ComfyUI commit、前端版本、节点版本、GPU、dtype、模型文件 SHA256、输入素材 SHA256、seed、全部参数。关闭运行后自动随机/递增 seed。先跑 A，再只改变一个参数跑 B，再恢复 A 做 A′。如果 A 与 A′ 不能复现，先解决这个问题。

对采样器、补丁、模型合并与训练，必须从同一未修改的源对象/权重开始。不能把上一次处理的结果继续叠加后宣称是独立对照。修改分支时确认目标节点及下游真的执行；ComfyUI 缓存命中不能证明重复计算确定性，也不能证明算子加速。

## 2. 四种预期，不用同一种标准验收

| 预期类型 | 例子 | 判定方式 |
|---|---|---|
| 精确值/结构 | 裁剪256×192、字符串结果、batch=3、mask严格大于阈值 | 尺寸/计数/文本精确相等；浮点按事先确定的容差 |
| 数值公式 | brightness=clamp(x×factor)、音量gain=10^(dB/20) | 选已知输入逐点算理论值；与实测比较 |
| 几何/结构关系 | bbox平移、帧顺序、首末关键帧时间、合并点数 | 量坐标、索引、时间戳、对象数，不能只看截图 |
| 统计倾向 | CFG、LoRA、ControlNet、参考图、模型补丁 | 5个固定seed配对，报告每个样本与汇总；允许没有改善 |

“参数更大→画质更好”不是可签收的预期。图像生成没有普遍单调性。seed变化也不保证每次输出一定不同；噪声关闭、缓存或条件退化都可能使输出不变。

## 3. 准备可测素材

```bash
python3 -m pip install -r tools/requirements-observe.txt
python3 tools/make_fixtures.py --out input/node-labs
```

生成 P1=512×384带文字/角标/坐标图案、P2三档透明度、纯色A/B、灰阶渐变、M1中央矩形、24张编号帧、440/880Hz低幅音频、三段不同频率音频与manifest。脚本只创建明确指定目录中的新文件；已存在时拒绝覆盖。运行位置应为自己的ComfyUI环境或复制生成文件到ComfyUI/input。生成素材无需GPU。

M1白矩形为 `x=[128,384), y=[96,288)`，宽256、高192。图片使用8bit，`128/255 ≠ 0.5`；测试阈值相等与精确中灰时，使用SolidMask的浮点0.5而不是PNG。

3D网格、Gaussian splat、MHR姿态、真实模型及训练数据**不包含在素材脚本中**；按对应卡片准备，未取得时标BLOCKED，不伪造已运行。

## 4. 哪个出口能看到什么

| 数据 | 可用检查方式 | 限制 |
|---|---|---|
| IMAGE | GetImageSize、PreviewImage、SaveImage后读PNG | PNG量化/截断，不能证明float tensor的负值与精确小数 |
| MASK | MaskToImage、MaskPreview、PNG像素/白区bbox | LoadImage的MASK往往为1-alpha；灰度PNG要显式ImageToMask取通道 |
| INT/FLOAT/STRING | PreviewAny | 字符串化摘要可能截断复杂对象 |
| LATENT/CONDITIONING/SIGMAS/NOISE | 本机源码断点或只读诊断打印 | 普通预览不能证明shape、metadata或实际噪声生成正确 |
| VIDEO/AUDIO | 解封装帧号、时间戳；音频波形/采样率/声道 | 有损编码与VAE往返不能要求逐样本相等 |
| MESH/SPLAT/FILE_3D | GetMeshInfo/GetSplatCount、独立3D导入器 | 自动居中会掩盖根平移/尺度变化；普通点云不等于Gaussian |
| MODEL/CLIP/HOOKS | 元数据/权重/实际消费时的日志 + 固定下游任务 | 对象非空不等于补丁生效；需要权重级断言时必须读权重 |

本项目没有增加第三方诊断节点。若缺少张量观察手段，该项记 `BLOCKED_OBSERVATION`。软件工程师可以在本机节点执行函数返回前临时设置断点，读取以下信息；完成后还原代码，**不要把诊断修改算成被测原版**：

```python
# 仅在已知局部变量 t 为 torch.Tensor 的调试断点中执行；不导出权重。
print(tuple(t.shape), t.dtype, t.device)
if t.numel():
    v = t.detach().float()
    print('finite', bool(v.isfinite().all()),
          'min/max', v.min().item(), v.max().item(),
          'mean/std', v.mean().item(), v.std(unbiased=False).item())
# LATENT通常先看samples，但联合AV latent可能是NestedTensor，需分别查看各分支。
# CONDITIONING要逐条查看embedding及metadata，不能只看一个总shape。
```

## 5. 可直接使用的文件测量

```bash
python3 tools/measure.py image input/node-labs/P1.png
python3 tools/measure.py image output/A.png --reference output/B.png
python3 tools/measure.py audio input/node-labs/A1.wav
```

输出JSON，包含图像尺寸、通道、范围、均值、颜色数、首通道非零bbox、图片差值MAE/最大误差；WAV输出采样率、通道、样本数、时长、peak/RMS、主频。测量工具只支持PCM16 WAV；其它编码先无损解码成PCM，不把不支持的格式报错算节点失败。

## 6. 容差先约定

- 确定性float32简单代数：最大绝对误差建议≤1e-6；复杂转换按源码精度单独约定。
- 8bit PNG：与理论归一化值比较通常允许1/255的量化误差。比较相同量化链路的恒等输出可要求像素相等。
- 刚体几何：建议误差≤1e-5×场景尺度；量化/简化/重网格必须另设误差预算。
- 视频：名义时长N/fps与首末样本跨度(N-1)/fps分开记录；封装时间基准通常允许1帧误差，丢帧不能混过去。
- 模型精度切换/有损VAE：没有通用通过阈值。先记录误差，再由该任务接受标准设阈值，不能事后为结果调整阈值。

## 7. 生成类怎样具体评分

以提示词 `a red cube on a white background` 为例，先定义三个独立0/1项：主体是立方体、主体为红色、背景为白色；另记录严重伪影0/1。seed固定为123、124、125、126、127，每个seed同时跑A/B。列出5对原图与评分，再汇总总分和胜/平/负。样本少，仅作为练习观察，不做统计显著性或质量保证。

控制/参考类按任务改评分：对象中心是否在指定半区、指定帧是否出现参考对象、关键点平均像素偏差、身份是否切换、主音调是否存在。必须事先写规则，不能生成后临时挑有利指标。

## 8. 无变化与失败如何排查

依次检查目标节点是否执行、参数是否在当前动态分支内生效、输出是否接到正确消费者、输入是否具有足够对比（常量图无法测模糊，静止相机平移无法测运动，单人无法测track_index=1）、LoRA/patch是否匹配实际权重。确认这些后仍违背确定性预期，标FAIL并附最小工作流；随机效果不显著可标INCONCLUSIVE，不能随意判通过。
