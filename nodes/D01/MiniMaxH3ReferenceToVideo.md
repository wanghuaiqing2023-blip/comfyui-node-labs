# MiniMaxH3ReferenceToVideo：可观察实验

[所属实验 D01](../../labs/04-minimax-h3/D01.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

匹配H3模型、CLIP、video VAE、audio VAE；1344×768,length=124；一张高分辨率人物参考；prompt明确引用<Picture 1>，固定seed。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| D01/MiniMaxH3ReferenceToVideo/01 | 同一ref_image_1换成另一人物，标签不变 | minimax_refs中图像参考块更新；生成主体身份倾向相应改变。输出positive和AV latent，没有负向条件输出。 | 先查参考块数量/类型，再5seed盲评主体特征；不能承诺身份绝对一致。 |
| D01/MiniMaxH3ReferenceToVideo/02 | ref_image_size=match → max | 高分辨率参考可能保留更大尺寸/更多token，耗时和显存可能上升；小图可能两种模式相同，因为不会任意上采样。 | 记录参考resize后宽高与token/latent网格；不要用小参考图验证两档差别。 |
| D01/MiniMaxH3ReferenceToVideo/03 | reference video依次4、5、21、22帧，输出length至少22 | 已核对版本：4帧报错；5合法；21裁到5；22保留22。参考视频按17k+5向下裁，区别于输出时长向上对齐。 | 先检查编码前帧数；参考视频期望24fps。不要只看最终视频时长。 |
| D01/MiniMaxH3ReferenceToVideo/04 | 视频参考附带同编号ref_video_audio_N，然后另接独立ref_audio | 视频音轨通过同编号配对；音频标签按呈现顺序独立编号，不能把Video编号直接等同Audio编号。 | 记录参考顺序/标签、音频采样率转换和metadata块kind。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| clip | CLIP | required | — |
| vae | VAE | required | — |
| audio_vae | VAE | required | — |
| prompt | STRING | required | 多行文本 |
| width | INT | required | 默认 1344；最小 32；最大 16384；步长 32 |
| height | INT | required | 默认 768；最小 32；最大 16384；步长 32 |
| length | INT | required | 默认 124；最小 5；最大 3600；步长 17；源码提示：Frame count at 24 fps, (124 = ~5s, trained range is ~124-362) |
| ref_image_size | COMBO | required | 默认 'match'；源码提示：Reference image sizing. 'match' scales each ref (down only, keeping aspect) to the generation's pixel area; 'max' uses the reference pipeline's 2048px short edge for best identity fidelity. Reference tokens ride through every sampling step, so 'max' can be several times slower. |
| ref_images | COMFY_AUTOGROW_V3 | optional | — |
| ref_videos | COMFY_AUTOGROW_V3 | optional | — |
| ref_video_audios | COMFY_AUTOGROW_V3 | optional | — |
| ref_audios | COMFY_AUTOGROW_V3 | optional | — |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| positive | CONDITIONING |
| LATENT | LATENT |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_minimax_h3`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
