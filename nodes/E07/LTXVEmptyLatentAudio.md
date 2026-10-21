# LTXVEmptyLatentAudio：可观察实验

[所属实验 E07](../../labs/05-model-families/E07.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

先完成所属实验组的上游闭环，保存一份冻结输入；模型文件、dtype、设备与随机种子都记录到实验表。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| E07/LTXVEmptyLatentAudio/01 | 诊断输入每帧/切片带编号；通过本节点 | 输出张量维度、帧顺序、noise_mask等元数据符合此操作；必须逐轴记录，不能只看LATENT类型相同。 | 查输入输出shape/编号；用对应解码器辅助观察。 |
| E07/LTXVEmptyLatentAudio/02 | 只改变本节点的一个时序/空间/噪声输入，恢复后再跑一次 | 裁切/替换应作用于明确区间，区间外编号保持；生成噪声应固定随机种子可复现；分块合并应保序且不丢帧。 | 按本节点名称选择操作；具体参数单位/轴未从源码确认前标待核对，不能标PASS。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| frames_number | INT | required | 默认 97；最小 1；最大 1000；步长 1；源码提示：Number of frames. |
| frame_rate | FLOAT,INT | required | 默认 25.0；最小 1.0；最大 1000.0；步长 0.01；源码提示：Number of frames per second. |
| batch_size | INT | required | 默认 1；最小 1；最大 4096；源码提示：The number of latent audio samples in the batch. |
| audio_vae | VAE | required | 源码提示：The Audio VAE model to get configuration from. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| Latent | LATENT |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_lt_audio`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
