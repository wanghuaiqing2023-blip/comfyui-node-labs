# ControlNetInpaintingAliMamaApply：可观察实验

[所属实验 B13](../../labs/02-generation/B13.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：应用 AliMama 局部重绘控制。**

- 用边缘、姿态、深度或其他控制信号约束生成时，用于应用 AliMama 局部重绘控制。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `positive` / `CONDITIONING` | 必需 | [CLIPTextEncode](../B01/CLIPTextEncode.md) → `CONDITIONING`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `negative` / `CONDITIONING` | 必需 | [CLIPTextEncode](../B01/CLIPTextEncode.md) → `CONDITIONING`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `control_net` / `CONTROL_NET` | 必需 | [ControlNetLoader](../B13/ControlNetLoader.md) → `CONTROL_NET`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `vae` / `VAE` | 必需 | [VAELoader](../B01/VAELoader.md) → `VAE`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `image` / `IMAGE` | 必需 | [LoadImage](../A01/LoadImage.md) → `IMAGE` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |
| `mask` / `MASK` | 必需 | [LoadImageMask](../A07/LoadImageMask.md) → `MASK`；[SolidMask](../A07/SolidMask.md) → `MASK` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |

**文本、数值与选项输入：** `strength`、`start_percent`、`end_percent`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[CLIPTextEncode](../B01/CLIPTextEncode.md)、[ControlNetLoader](../B13/ControlNetLoader.md)、[VAELoader](../B01/VAELoader.md)、[LoadImage](../A01/LoadImage.md)、[LoadImageMask](../A07/LoadImageMask.md)、[SolidMask](../A07/SolidMask.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

先完成所属实验组的上游闭环，保存一份冻结输入；模型文件、dtype、设备与随机种子都记录到实验表。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| B13/ControlNetInpaintingAliMamaApply/01 | 固定所有模型，按输入表连接基准条件，保存条件摘要 | 必须产出下表声明的端口；正负条件、latent、音视频分支的返回数量按当前节点逐一核对。不允许假设每个条件节点都同时输出positive/negative/latent。 | 记录每个CONDITIONING条目数、shape、metadata key、引用帧号及latent各轴。 |
| B13/ControlNetInpaintingAliMamaApply/02 | 仅替换参考输入 image, mask 中的一项 | 对应参考/区域/时序metadata改变；生成的参考符合程度只能统计比较，不能保证整幅画面逐像素跟随。参考类型必须与模型家族匹配。 | 用明显不同且合法的两份参考；同5seed比较参考主体、布局/动作/声音中的目标属性。若只改时间配置，直接查时间字段。 |
| B13/ControlNetInpaintingAliMamaApply/03 | 仅改strength为默认值与一个邻近合法值 | 该条件/噪声/引导权重发生变化；若源码明确0是关闭，可补0组。不能把所有strength/noise_augmentation都解释为越大越贴近参考。 | 记录直接条件权重或噪声幅度；配对结果分开评价符合程度与伪影。 |
| B13/ControlNetInpaintingAliMamaApply/04 | 单参数数值扫描：strength = 0.75 → 1 → 1.25（其它保持基准） | 所选模块/条件/补丁的系数改变；具体中性值由节点算法决定。可观察目标是配置/权重增量及固定输入的响应，画质没有通用单调方向。 | 先查strength进入的权重/condition/前向配置；再5seed记录目标属性分数和伪影。 |
| B13/ControlNetInpaintingAliMamaApply/05 | 单参数数值扫描：start_percent = 0 → 0.001（其它保持基准） | 所选作用时间区间边界移动；按sigma映射判断生效步，不直接用percent×steps代替。 | 确保start≤end；打印每步生效标志。与另一个边界冲突的数值跳过并记录。 |
| B13/ControlNetInpaintingAliMamaApply/06 | 单参数数值扫描：end_percent = 0.75 → 1（其它保持基准） | 所选作用时间区间边界移动；按sigma映射判断生效步，不直接用percent×steps代替。 | 确保start≤end；打印每步生效标志。与另一个边界冲突的数值跳过并记录。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| positive | CONDITIONING | required | — |
| negative | CONDITIONING | required | — |
| control_net | CONTROL_NET | required | — |
| vae | VAE | required | — |
| image | IMAGE | required | — |
| mask | MASK | required | — |
| strength | FLOAT | required | 默认 1.0；最小 0.0；最大 10.0；步长 0.01 |
| start_percent | FLOAT | required | 默认 0.0；最小 0.0；最大 1.0；步长 0.001 |
| end_percent | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.001 |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| positive | CONDITIONING |
| negative | CONDITIONING |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_controlnet`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
