# WanAnimate2ToVideo：可观察实验

[所属实验 E14](../../labs/05-model-families/E14.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

先完成所属实验组的上游闭环，保存一份冻结输入；模型文件、dtype、设备与随机种子都记录到实验表。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| E14/WanAnimate2ToVideo/01 | 固定所有模型，按输入表连接基准条件，保存条件摘要 | 必须产出下表声明的端口；正负条件、latent、音视频分支的返回数量按当前节点逐一核对。不允许假设每个条件节点都同时输出positive/negative/latent。 | 记录每个CONDITIONING条目数、shape、metadata key、引用帧号及latent各轴。 |
| E14/WanAnimate2ToVideo/02 | 仅替换参考输入 reference_image, pose_video, clip_vision_output, clip_vision_output_pose, continue_motion 中的一项 | 对应参考/区域/时序metadata改变；生成的参考符合程度只能统计比较，不能保证整幅画面逐像素跟随。参考类型必须与模型家族匹配。 | 用明显不同且合法的两份参考；同5seed比较参考主体、布局/动作/声音中的目标属性。若只改时间配置，直接查时间字段。 |
| E14/WanAnimate2ToVideo/03 | 仅改pose_strength为默认值与一个邻近合法值 | 该条件/噪声/引导权重发生变化；若源码明确0是关闭，可补0组。不能把所有strength/noise_augmentation都解释为越大越贴近参考。 | 记录直接条件权重或噪声幅度；配对结果分开评价符合程度与伪影。 |
| E14/WanAnimate2ToVideo/04 | 单参数数值扫描：width = 624 → 832 → 1040（其它保持基准） | 输出latent的空间宽轴应按本模型压缩/对齐规则变化；高度与时间轴保持。先用匹配解码器检查最终宽度。 | 每次记录直接输出shape/对应metadata；取整规则未知时先核对模型配置，不能套用SD的8倍。 |
| E14/WanAnimate2ToVideo/05 | 单参数数值扫描：length = 61 → 81 → 101（其它保持基准） | 目标帧数按模型合法时间网格对齐，视频帧数改变；空间尺寸保持。 | 导出实际帧数/样本数与时间戳；检查音画同步，不能只读播放器舍入秒数。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| positive | CONDITIONING | required | — |
| negative | CONDITIONING | required | — |
| vae | VAE | required | — |
| width | INT | required | 默认 832；最小 16；最大 16384；步长 16；源码提示：Output video width in pixels. |
| height | INT | required | 默认 480；最小 16；最大 16384；步长 16；源码提示：Output video height in pixels. |
| length | INT | required | 默认 81；最小 1；最大 16384；步长 4；源码提示：Number of frames to generate. |
| batch_size | INT | required | 默认 1；最小 1；最大 4096；源码提示：Number of videos to generate simultaneously. |
| video_frame_offset | INT | required | 默认 0；最小 0；最大 16384；步长 1；源码提示：Frames to seek into the pose video. Connect to the video_frame_offset output of the previous node when extending. |
| pose_strength | FLOAT | required | 默认 1.0；最小 0.0；最大 10.0；步长 0.01；源码提示：Scales the pose video's influence on the motion. 1.0 is the trained behavior; below weakens adherence, above amplifies. 0.0 mutes it but does not fully remove it. |
| pose_start_percent | FLOAT | required | 默认 0.0；最小 0.0；最大 1.0；步长 0.01；源码提示：Sampling percent at which the pose influence starts. Outside the window the pose branch is skipped entirely, which also speeds those steps up. |
| pose_end_percent | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01；源码提示：Sampling percent at which the pose influence ends. Motion is mostly established early, so e.g. 0.7 can loosen fine detail while keeping the choreography. |
| reference_image_strength | FLOAT | required | 默认 1.0；最小 0.0；最大 10.0；步长 0.01；源码提示：Scales how strongly generated frames attend to the reference image's latent frame. Below 1.0 loosens identity/appearance adherence (e.g. to let the prompt restyle), above tightens it against drift. |
| reference_image | IMAGE | optional | 源码提示：The character to animate. |
| pose_video | IMAGE | optional | 源码提示：The video whose motion is transferred to the reference character. |
| clip_vision_output | CLIP_VISION_OUTPUT | optional | 源码提示：CLIP vision of the reference image. |
| positive_pose | CONDITIONING | optional | 源码提示：Prompt for the pose-video branch, describing the motion rather than the character. Defaults to positive. Used for both the cond and uncond passes. |
| clip_vision_output_pose | CLIP_VISION_OUTPUT | optional | 源码提示：CLIP vision of the pose video's first frame. Defaults to clip_vision_output. |
| continue_motion | IMAGE | optional | 源码提示：Previous motion sequence to continue from for temporal consistency. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| positive | CONDITIONING |
| negative | CONDITIONING |
| latent | LATENT |
| trim_latent | INT |
| trim_image | INT |
| video_frame_offset | INT |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_wan`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
