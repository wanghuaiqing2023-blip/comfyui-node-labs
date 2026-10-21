# BuildPoseFile 的完整实验依赖

[项目首页](../README.md) · [阅读指南](README.md)

| 步骤 | 节点与连接 | 先观察什么 |
|---|---|---|
| 1 | LoadVideo→GetVideoComponents | 帧数、FPS、是否有有效视频内容 |
| 2 | SAM3DBody_Loader→SAM3DBody_Predict.sam3d_body_model | 人体模型正确加载 |
| 3 | GetVideoComponents.images→SAM3DBody_Predict.image | 输入帧顺序与人物可见性 |
| 4 | 可选检测框→Predict.bboxes；多人跟踪→Predict.track_data | 框、track 与人物对应 |
| 5 | Predict.mhr_pose_data→SAM3DBody_Render.pose_data | 原始姿态是否合理 |
| 6 | Predict.mhr_pose_data→SAM3DBody_Smooth→同一 Render | 静止抖动与快速动作是否被过度平滑 |
| 7 | 已确认的 pose_data→BuildPoseFile；按输出分支连接人体模型 | 导出的动作是否与渲染一致 |
| 8 | BuildPoseFile.model_3d→本机支持 FILE_3D 的保存节点 | 实际落盘格式、动画时长、可回读性 |

[F10](../labs/06-vision-3d/F10.md) 子实验顺序：GLB 基线 → fps 12/24/48 → off/centered/absolute → GLB 表示样式 → 单人与多人轨迹选择 → BVH → 条件模型输入缺失的诊断。

相同 N 个时间采样的首末关键帧跨度通常按 (N−1)/fps 预测；容器播放时长可能按 N/fps 展示，先看相对比例。camera_translation 是否有差异取决于 pose_data 内的预测平移，不能用没有位移的数据检验“侧移保留”。

单纯渲染姿态做动作控制可以走 Render→IMAGE→视频模型，不必绕到导出动画再导入。BuildPoseFile 服务于三维动画资产交付与进一步编辑。
