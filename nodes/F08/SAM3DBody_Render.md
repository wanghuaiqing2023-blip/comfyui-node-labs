# SAM3DBody_Render：可观察实验

[所属实验 F08](../../labs/06-vision-3d/F08.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：渲染人体姿态预测结果。**

- 从人物素材获得可渲染的三维姿态时，用于渲染人体姿态预测结果。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `pose_data` / `MHR_POSE_DATA,KIMODO_POSE_DATA` | 必需 | [SAM3DBody_Predict](../F08/SAM3DBody_Predict.md) → `mhr_pose_data`；[SAM3DBody_Smooth](../F09/SAM3DBody_Smooth.md) → `mhr_pose_data` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 表中示例仅覆盖 MHR；固定索引缺 Kimodo 生产者。 |
| `render_style` / `COMFY_DYNAMICCOMBO_V3` | 必需 | 本节点模式选择 / 展开的子输入 | 本节点选择模式并展开子参数；子输入依赖随所选模式变化，固定索引未展开全部分支。 |
| `background` / `IMAGE` | 可选 | [LoadImage](../A01/LoadImage.md) → `IMAGE` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |
| `camera_info` / `LOAD3D_CAMERA` | 可选 | [CreateCameraInfo](../F01/CreateCameraInfo.md) → `camera_info`；[Load3DAdvanced](../F01/Load3DAdvanced.md) → `camera_info` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |

**文本、数值与选项输入：** `width`、`height`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[SAM3DBody_Predict](../F08/SAM3DBody_Predict.md)、[SAM3DBody_Smooth](../F09/SAM3DBody_Smooth.md)、[LoadImage](../A01/LoadImage.md)、[CreateCameraInfo](../F01/CreateCameraInfo.md)、[Load3DAdvanced](../F01/Load3DAdvanced.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

P3：单人24帧抬手侧移，固定相机；Predict使用同一模型，Render使用冻结pose_data。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| F08/SAM3DBody_Render/01 | Predict只切run_hand_refinement；Render只切render_style | 前者主要影响手部估计/耗时，不保证总误差下降；后者只改变表示，不应改变同帧动作阶段。 | 逐帧看手腕/指尖及人物数量；不同节点不要同时改动。 |
| F08/SAM3DBody_Render/02 | Render宽高512×512→1024×512 | 输出尺寸改变，pose_data本身不变。 | 通过GetImageSize验证；Predict无width参数则不做该项。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| pose_data | MHR_POSE_DATA,KIMODO_POSE_DATA | required | 源码提示：MHR pose data, or external Y-up rig pose data (KimodoSample). All render styles work for external rigs that carry OpenPose joint maps in their _skeleton_override (KimodoSample does). |
| width | INT | required | 默认 0；最小 0；最大 16384；步长 8；源码提示：Output width in pixels. 0 = use pose data's native image_size. If only one of width/height is set, the other is derived preserving the original aspect. |
| height | INT | required | 默认 0；最小 0；最大 16384；步长 8；源码提示：Output height in pixels. 0 = use pose data's native image_size. If only one of width/height is set, the other is derived preserving the original aspect. |
| render_style | COMFY_DYNAMICCOMBO_V3 | required | 源码提示：'mesh' = 3D MHR mesh rasterized through the camera. 'silhouette' = binary mask of the mesh. 'openpose_2d' = flat 2D skeleton 'openpose_3d' = openpose skeleton as flat-shaded 3D model 'scail' = SCAIL 3D capsules |
| background | IMAGE | optional | 源码提示：Per-frame background. Omitted = black canvas. |
| camera_info | LOAD3D_CAMERA | optional | 源码提示：Free 6DOF camera override. When wired, the pose is re-projected through this camera (position/target/zoom/rotation/FoV) instead of the predicted one. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| image | IMAGE |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_sam3d_body`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
