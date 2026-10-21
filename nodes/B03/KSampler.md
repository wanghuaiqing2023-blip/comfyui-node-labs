# KSampler：可观察实验

[所属实验 B03](../../labs/02-generation/B03.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：将模型条件与潜变量送入一体化采样过程。**

- 从空潜变量开始，根据提示词生成图片。
- 把输入图编码成潜变量后进行图生图，通过 denoise 控制允许改变的幅度。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `model` / `MODEL` | 必需 | [UNETLoader](../B01/UNETLoader.md) → `MODEL`（兼容性候选）；[CheckpointLoaderSimple](../B01/CheckpointLoaderSimple.md) → `MODEL`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `positive` / `CONDITIONING` | 必需 | [CLIPTextEncode](../B01/CLIPTextEncode.md) → `CONDITIONING`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `negative` / `CONDITIONING` | 必需 | [CLIPTextEncode](../B01/CLIPTextEncode.md) → `CONDITIONING`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `latent_image` / `LATENT` | 必需 | [EmptyLatentImage](../B03/EmptyLatentImage.md) → `LATENT`（兼容性候选）；[VAEEncode](../B02/VAEEncode.md) → `LATENT`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |

**文本、数值与选项输入：** `seed`、`steps`、`cfg`、`sampler_name`、`scheduler`、`denoise`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[UNETLoader](../B01/UNETLoader.md)、[CheckpointLoaderSimple](../B01/CheckpointLoaderSimple.md)、[CLIPTextEncode](../B01/CLIPTextEncode.md)、[EmptyLatentImage](../B03/EmptyLatentImage.md)、[VAEEncode](../B02/VAEEncode.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

使用已跑通的 SD1.5 基线：512×512，batch=1，euler，normal，steps=20，cfg=7，seed=123 fixed，denoise=1；提示词 red cube on white background。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| B03/KSampler/01 | 所有输入固定，重复运行，再 seed=124 | 同环境重复运行应可复现（GPU非确定性单列）；换seed通常改变构图/纹理，尺寸保持512×512。 | 分别保存结果，MAE对照；缓存命中不是重新计算证据。 |
| B03/KSampler/02 | steps=10 → 20 → 30 | 采样步数预算提高；耗时通常增加。画质和提示词遵循度没有必然单调关系。 | 记录采样时间而非加载时间；同seed并排，评估对象/颜色/背景三项。 |
| B03/KSampler/03 | cfg=1 → 4 → 8，steps固定 | 普通CFG模型的条件/无条件组合权重改变；高值可能更强调条件，也可能过饱和/失真。 | 用5个固定seed配对比较三项符合率及失真数；不能由一张图判定规律。 |
| B03/KSampler/04 | 输入改为已编码P1后，仅denoise=0 → 0.3 → 0.7 → 1 | 0时latent保留；较高值通常允许更大改动，非严格单调。0组与P1的VAE往返图比较，不与原PNG要求相等。 | 固定同一latent和seed；保存差值及内容变化。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| model | MODEL | required | 源码提示：The model used for denoising the input latent. |
| seed | INT | required | 默认 0；最小 0；最大 18446744073709551615；源码提示：The random seed used for creating the noise. |
| steps | INT | required | 默认 20；最小 1；最大 10000；源码提示：The number of steps used in the denoising process. |
| cfg | FLOAT | required | 默认 8.0；最小 0.0；最大 100.0；步长 0.1；源码提示：The Classifier-Free Guidance scale balances creativity and adherence to the prompt. Higher values result in images more closely matching the prompt however too high values will negatively impact quality. |
| sampler_name | COMBO | required | 选项：'euler'、'euler_cfg_pp'、'euler_ancestral'、'euler_ancestral_cfg_pp'、'heun'、'heunpp2'、'exp_heun_2_x0'、'exp_heun_2_x0_sde'、'dpm_2'、'dpm_2_ancestral'，另有 34 项；源码提示：The algorithm used when sampling, this can affect the quality, speed, and style of the generated output. |
| scheduler | COMBO | required | 选项：'simple'、'sgm_uniform'、'karras'、'exponential'、'ddim_uniform'、'beta'、'normal'、'linear_quadratic'、'kl_optimal'；源码提示：The scheduler controls how noise is gradually removed to form the image. |
| positive | CONDITIONING | required | 源码提示：The conditioning describing the attributes you want to include in the image. |
| negative | CONDITIONING | required | 源码提示：The conditioning describing the attributes you want to exclude from the image. |
| latent_image | LATENT | required | 源码提示：The latent image to denoise. |
| denoise | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01；源码提示：The amount of denoising applied, lower values will maintain the structure of the initial image allowing for image to image sampling. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| LATENT | LATENT |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`nodes`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
