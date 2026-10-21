# BuildPoseFile：可观察实验

[所属实验 F10](../../labs/06-vision-3d/F10.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：把人体姿态导出为动画 GLB 或 BVH 动捕文件。**

- 将人物动作预测结果导出为带动画的 GLB，在三维查看器中检查并交付。
- 需要把单人骨架动作交给动画软件继续制作时导出 BVH；材质与蒙皮交付要求另行核对。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `pose_data` / `MHR_POSE_DATA,KIMODO_POSE_DATA` | 必需 | [SAM3DBody_Smooth](../F09/SAM3DBody_Smooth.md) → `mhr_pose_data`；[SAM3DBody_Predict](../F08/SAM3DBody_Predict.md) → `mhr_pose_data` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 表中示例仅覆盖 MHR；固定索引缺 Kimodo 生产者。 |
| `format` / `COMFY_DYNAMICCOMBO_V3` | 必需 | 本节点模式选择 / 展开的子输入 | 本节点选择模式并展开子参数；子输入依赖随所选模式变化，固定索引未展开全部分支。 |
| `sam3d_body_model` / `SAM3D_BODY_MODEL` | 可选 | [SAM3DBody_Loader](../F08/SAM3DBody_Loader.md) → `sam3d_body_model` | 接口标 optional，但 MHR 的 BVH/网格/骨骼等分支可能需要模型；具体条件和无模型负例见本页用例。 |

**文本、数值与选项输入：** `fps`、`camera_translation`、`track_index`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[SAM3DBody_Smooth](../F09/SAM3DBody_Smooth.md)、[SAM3DBody_Predict](../F08/SAM3DBody_Predict.md)、[SAM3DBody_Loader](../F08/SAM3DBody_Loader.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

固定24帧MHR姿态，单人抬手并侧移；另备2条有效track；连同一SAM3D_BODY_MODEL；GLB先用body_mesh；固定世界相机，关闭自动居中。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| F10/BuildPoseFile/01 | fps=12 → 24 → 48，其余完全相同 | 关键帧间隔1/12→1/24→1/48秒；24帧首尾采样时间跨度23/fps，即1.916667、0.958333、0.479167秒。按N/fps计片段名义时长则为2、1、0.5秒，两种口径不能混淆。 | 读取GLB animation时间accessor或BVH Frame Time；同帧姿态应保持，禁止只凭播放快慢。 |
| F10/BuildPoseFile/02 | camera_translation=off → centered → absolute | off不烘焙预测相机平移；centered使用相对首帧位移，首帧增量0；absolute使用原始平移，可能有较大Z深度。这里只比较新增的平移项，不要求骨架root世界坐标为0。 | 记录首/中/末帧root平移向量；固定相机截图。若输入平移恒定，centered看不出运动，应更换侧移素材。 |
| F10/BuildPoseFile/03 | 2条轨迹下track_index=-1 → 0 → 1 | GLB分别导出全部/第一条/第二条；应能通过抬左手与抬右手动作辨别。BVH只支持单骨架，-1在已核对源码中退化为0。 | 数人体实例/骨架并核对动作，不能只数mesh节点（单人可能多mesh）。 |
| F10/BuildPoseFile/04 | format=glb → bvh；BVH units=m → cm | GLB可带网格/材质/骨骼动画；BVH为层级与运动，不保留材质。cm与m长度/平移数值应相差100倍，旋转与帧数不变。 | BVH检查HIERARCHY、MOTION、Frames=24、Frame Time=1/fps；设置导入单位后比较世界尺度。 |
| F10/BuildPoseFile/05 | MHR输入且无_skeleton_override；断开sam3d_body_model，选择bvh/body_mesh/bones_only | 应明确报告缺少模型/骨架，不应产出有效空文件；这些分支虽顶层optional，运行时仍有条件依赖。 | 记录完整异常并恢复连接重试；此失败是预期负例。 |
| F10/BuildPoseFile/06 | GLB mesh_style：body_mesh → bones_only → openpose/scail | 表示方式改变：皮肤网格、骨骼、关键点/连杆；相同帧的动作阶段仍对应。细分材质、骨骼半径、手脸开关须记录展开后的实际字段。 | 核对几何/材质、关键帧与坐标，不把风格变化当成pose推理变化。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| pose_data | MHR_POSE_DATA,KIMODO_POSE_DATA | required | 源码提示：3D pose data. |
| format | COMFY_DYNAMICCOMBO_V3 | required | 源码提示：Output format, both fed to Save 3D Model to write to disk. 'glb' = animated GLB (mesh / bones / openpose / scail). 'bvh' = BVH mocap clip (one skeleton; needs the model). |
| fps | FLOAT | required | 默认 24.0；最小 1.0；最大 240.0；步长 1.0；源码提示：Animation frame rate. |
| camera_translation | COMBO | required | 默认 'off'；源码提示：Bake pred_cam_t into the root's translation 'off' = bind position 'centered' = delta from frame 0 'absolute' = raw (Z is camera depth — usually meters away). |
| track_index | INT | required | 默认 -1；最小 -1；最大 15；源码提示：-1 = all tracks; ≥0 = single track. |
| sam3d_body_model | SAM3D_BODY_MODEL | optional | — |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| model_3d | FILE_3D |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_sam3d_body`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
