# CreateCameraInfo：可观察实验

[所属实验 F01](../../labs/06-vision-3d/F01.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

不对称三维标尺：X/Y/Z方向有颜色标记；固定target=(0,0,0)、roll=0、zoom=1，透视相机。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| F01/CreateCameraInfo/01 | fov=35 → 70度 | 同一相机位置下视野扩大，物体投影通常变小；世界坐标/几何不变。 | 固定RenderMesh/RenderSplat，测物体像素包围框。 |
| F01/CreateCameraInfo/02 | zoom=1 → 2；fov恢复35 | 画面放大，物体可能被裁出画布；相机位置保持。 | 记录camera_info与角标位置，不同时改distance。 |
| F01/CreateCameraInfo/03 | roll=0 → 90度 | 画面绕视线轴旋转；不是物体绕世界Y轴转。 | 检查Y-up和右手系；截图保存坐标轴。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| mode | COMFY_DYNAMICCOMBO_V3 | required | 源码提示：How to define the camera: orbit angles, an explicit position, or a position + quaternion. |
| target_x | FLOAT | required | 默认 0.0；最小 -1000.0；最大 1000.0；步长 0.01；源码提示：Look-at point (orbit pivot / aim). In orbit mode, move it to pan/translate the whole camera. Ignored in quaternion mode. Defaults to the origin. |
| target_y | FLOAT | required | 默认 0.0；最小 -1000.0；最大 1000.0；步长 0.01 |
| target_z | FLOAT | required | 默认 0.0；最小 -1000.0；最大 1000.0；步长 0.01 |
| roll | FLOAT | required | 默认 0.0；最小 -180.0；最大 180.0；步长 1.0；源码提示：Camera roll about the view axis, degrees. |
| fov | FLOAT | required | 默认 35.0；最小 1.0；最大 120.0；步长 1.0；源码提示：Vertical field of view in degrees. |
| zoom | FLOAT | required | 默认 1.0；最小 0.01；最大 100.0；步长 0.01；源码提示：Digital zoom (focal-length multiplier). &gt;1 zooms in without moving the camera. |
| camera_type | COMBO | required | 源码提示：Projection used by Render Splat: perspective (foreshortening) or orthographic (parallel). |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| camera_info | LOAD3D_CAMERA |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_gaussian_splat`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
