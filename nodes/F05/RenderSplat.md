# RenderSplat：可观察实验

[所属实验 F05](../../labs/06-vision-3d/F05.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：渲染 splat 检查结果。**

- 检查、变换或交付 Gaussian Splat时，用于渲染 splat 检查结果。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `splat` / `SPLAT` | 必需 | [File3DToSplat](../F05/File3DToSplat.md) → `splat`；[VAEDecodeTripoSplat](../E19/VAEDecodeTripoSplat.md) → `splat` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |
| `background` / `COLOR` | 必需 | 本节点前端控件 | 颜色控件（按当前界面填写）提供状态；不是缺失的模型加载器。 |
| `bg_image` / `IMAGE` | 可选 | [LoadImage](../A01/LoadImage.md) → `IMAGE` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |
| `camera_info` / `LOAD3D_CAMERA` | 可选 | [CreateCameraInfo](../F01/CreateCameraInfo.md) → `camera_info`；[Load3DAdvanced](../F01/Load3DAdvanced.md) → `camera_info` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |

**文本、数值与选项输入：** `width`、`height`、`frames`、`splat_scale`、`sharpen`、`headlight_shading`、`opacity_threshold`、`render_style`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[File3DToSplat](../F05/File3DToSplat.md)、[VAEDecodeTripoSplat](../E19/VAEDecodeTripoSplat.md)、[LoadImage](../A01/LoadImage.md)、[CreateCameraInfo](../F01/CreateCameraInfo.md)、[Load3DAdvanced](../F01/Load3DAdvanced.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

G1或已知尺度S1，固定CreateCameraInfo和背景。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| F05/RenderSplat/01 | width=512,height=512 → width=1024,height=512 | 输出IMAGE/MASK尺寸对应设定；三维数据本身不变。 | GetImageSize，遮罩范围与物体投影对齐。 |
| F05/RenderSplat/02 | 只改background黑→白 | 物体外背景改变；遮罩几何范围应基本保持。 | MASK和RGB分别保存；透明边缘混色可变化。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| splat | SPLAT | required | — |
| width | INT | required | 默认 1024；最小 64；最大 2048；步长 8 |
| height | INT | required | 默认 1024；最小 64；最大 2048；步长 8 |
| frames | INT | required | 默认 1；最小 -240；最大 240；源码提示：-1, 0, 1 = single still image; &gt;1 = turntable, the camera orbits over a full 360 turn (works with any camera_info). Negative value orbits the other way. |
| splat_scale | FLOAT | required | 默认 1.0；最小 0.1；最大 5.0；步长 0.05；源码提示：Multiplier on each splat's projected footprint (lower = crisper points, higher = softer/fuller surface). |
| sharpen | FLOAT | required | 默认 2.0；最小 1.0；最大 8.0；步长 0.5；源码提示：Sharpen overlapping splats: 1.0 = physically-correct blend; higher biases each pixel toward its dominant (nearest) splat for crisper texture, without shrinking splats or opening gaps. Non-physical above 1. |
| headlight_shading | FLOAT | required | 默认 0.0；最小 0.0；最大 3.0；步长 0.05；源码提示：Diffuse shading from a light at the camera (headlight), using the splat surfel normals: darkens surfaces that turn away from view to reveal form/curvature. 0 = flat albedo, 1 = strongest shading. |
| opacity_threshold | FLOAT | required | 默认 0.0；最小 0.0；最大 1.0；步长 0.01；源码提示：Cull gaussians with opacity below this (removes faint floaters). |
| render_style | COMBO | required | 源码提示：What the image output shows: color, clay (neutral-albedo shaded), depth (near=bright), normal (OpenGL normal map). |
| background | COLOR | required | 默认 '#000000' |
| bg_image | IMAGE | optional | 源码提示：Optional background plate composited behind the splat (overrides the solid background colour). Resized to the render size; a batch is used per frame, a single image for all. color/clay only. |
| camera_info | LOAD3D_CAMERA | optional | 源码提示：Camera to render from - a Load3D / Preview3D camera or a Create Camera Info node. If empty, the splat is auto-framed from a default 3/4 view. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| image | IMAGE |
| mask | MASK |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_gaussian_splat`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
