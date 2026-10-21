# MiniMaxH3ReferenceToVideo：可观察实验

[所属实验 D01](../../labs/04-minimax-h3/D01.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：把图像视频音频参考组织为 H3 条件和初始潜变量。**

- 把角色参考图、动作参考视频或参考音频组织成 H3 条件，供后续采样生成视频。
- 多参考素材需要按编号在提示词中引用时，集中维护参考输入与标签对应关系。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `clip` / `CLIP` | 必需 | [CLIPLoader](../B01/CLIPLoader.md) → `CLIP`（兼容性候选）；[DualCLIPLoader](../B01/DualCLIPLoader.md) → `CLIP`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `vae` / `VAE` | 必需 | [VAELoader](../B01/VAELoader.md) → `VAE`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `audio_vae` / `VAE` | 必需 | [VAELoader](../B01/VAELoader.md) → `VAE`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `ref_images` / `COMFY_AUTOGROW_V3` | 可选 | [LoadImage](../A01/LoadImage.md) → `IMAGE`（展开后核对） | 动态/通配接口：先在当前界面展开实际子端口，再核对类型、数量及列表语义；候选不代表顶层可直接连线。 |
| `ref_videos` / `COMFY_AUTOGROW_V3` | 可选 | [GetVideoComponents](../C01/GetVideoComponents.md) → `images`（展开后核对） | 动态/通配接口：先在当前界面展开实际子端口，再核对类型、数量及列表语义；候选不代表顶层可直接连线。 已核对项目留存 H3 源码：ref_video_* 子端口接 IMAGE 帧批次，按 24 FPS 准备，不直接接 VIDEO。 |
| `ref_video_audios` / `COMFY_AUTOGROW_V3` | 可选 | [GetVideoComponents](../C01/GetVideoComponents.md) → `audio`（展开后核对） | 动态/通配接口：先在当前界面展开实际子端口，再核对类型、数量及列表语义；候选不代表顶层可直接连线。 音轨必须与同编号参考视频对应，不能任意拿另一段声音代替。 |
| `ref_audios` / `COMFY_AUTOGROW_V3` | 可选 | [LoadAudio](../C03/LoadAudio.md) → `AUDIO`（展开后核对） | 动态/通配接口：先在当前界面展开实际子端口，再核对类型、数量及列表语义；候选不代表顶层可直接连线。 |

**文本、数值与选项输入：** `prompt`、`width`、`height`、`length`、`ref_image_size`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[CLIPLoader](../B01/CLIPLoader.md)、[DualCLIPLoader](../B01/DualCLIPLoader.md)、[VAELoader](../B01/VAELoader.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

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
