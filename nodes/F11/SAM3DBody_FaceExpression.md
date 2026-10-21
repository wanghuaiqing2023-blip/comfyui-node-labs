# SAM3DBody_FaceExpression：可观察实验

[所属实验 F11](../../labs/06-vision-3d/F11.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：将面部表情信息应用到人体姿态。**

- 处理人体动作中的脸部区域与表情时，用于将面部表情信息应用到人体姿态。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `sam3d_body_model` / `SAM3D_BODY_MODEL` | 必需 | [SAM3DBody_Loader](../F08/SAM3DBody_Loader.md) → `sam3d_body_model` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |
| `mhr_pose_data` / `MHR_POSE_DATA` | 必需 | [SAM3DBody_Predict](../F08/SAM3DBody_Predict.md) → `mhr_pose_data`；[SAM3DBody_Smooth](../F09/SAM3DBody_Smooth.md) → `mhr_pose_data` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |
| `image` / `IMAGE` | 必需 | [LoadImage](../A01/LoadImage.md) → `IMAGE` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |

**文本、数值与选项输入：** `strength`、`mouth_strength`、`eye_strength`、`brow_strength`、`input_threshold`、`blendshape_smooth_window`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[SAM3DBody_Loader](../F08/SAM3DBody_Loader.md)、[SAM3DBody_Predict](../F08/SAM3DBody_Predict.md)、[SAM3DBody_Smooth](../F09/SAM3DBody_Smooth.md)、[LoadImage](../A01/LoadImage.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

短片依次闭嘴→张嘴→眨眼；另一张无脸照片作负例。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| F11/SAM3DBody_FaceExpression/01 | 目标区域/strength或绘制参数做单项变化 | FaceMask选mouth只覆盖嘴区；Visualize只改颜色/粗细不改变landmark坐标；FaceExpression mouth_strength增强应主要影响嘴部驱动。 | 固定同帧对照；Landmarker阈值变化记录检测数，不承诺全部帧命中。 |
| F11/SAM3DBody_FaceExpression/02 | 输入无脸帧，选择missing_frame_fallback（若存在） | 按fallback返回空/复用/错误中的实际约定；不能把上一帧复用误当本帧成功检测。 | 记录原始检测标记与最终显示分开。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| sam3d_body_model | SAM3D_BODY_MODEL | required | — |
| mhr_pose_data | MHR_POSE_DATA | required | — |
| image | IMAGE | required | — |
| strength | FLOAT | required | 默认 1.0；最小 0.0；最大 4.0；步长 0.05；源码提示：Global multiplier on all blendshapes. &gt;1 exaggerates. |
| mouth_strength | FLOAT | required | 默认 1.0；最小 0.0；最大 4.0；步长 0.05；源码提示：Multiplier on mouth/jaw shapes. MediaPipe's jawOpen saturates near 1.0. |
| eye_strength | FLOAT | required | 默认 2.0；最小 0.0；最大 4.0；步长 0.05；源码提示：Multiplier on eye shapes. MediaPipe rarely exceeds 0.5; 2-3x often needed. |
| brow_strength | FLOAT | required | 默认 2.0；最小 0.0；最大 4.0；步长 0.05；源码提示：Multiplier on brow/cheek/sneer shapes. MediaPipe outputs ~0.1-0.3; 2-3x. |
| input_threshold | FLOAT | required | 默认 0.02；最小 0.0；最大 0.5；步长 0.01；源码提示：Deadzone on MediaPipe's raw output (below = zero, above = linear remap). |
| blendshape_smooth_window | INT | required | 默认 7；最小 1；最大 31；步长 2；源码提示：Gaussian window on MediaPipe's per-frame signal before MHR mapping. MediaPipe's raw output swings 30-70% frame-to-frame on static faces. 1 = disabled. Use odd values. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| mhr_pose_data | MHR_POSE_DATA |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_sam3d_body`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
