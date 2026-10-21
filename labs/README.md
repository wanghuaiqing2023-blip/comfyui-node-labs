# 全部实验

[项目首页](../README.md) · [学习路线](../guides/learning-path.md) · [节点索引](../node-index/README.md)

[前置练习：前端与画布操作 U01—U04](00-frontend/README.md) 共 4 组、18 个用例，建议先完成，再进入下表。它们独立于 639 个后端节点的覆盖统计。

以下为 78 个后端实验组，每组一页。下表保持原手册的前置能力顺序；模型分支按需要选做，不要求全部依次运行。

| 顺序 | 实验组 | 前置能力 | 节点数 |
|---:|---|---|---:|
| 1 | [A01 建立观察与保存出口](01-basics/A01.md) | 无 | 7 |
| 2 | [A02 把参数变成数据](01-basics/A02.md) | [A01](01-basics/A01.md) | 13 |
| 3 | [A03 确定性文本处理](01-basics/A03.md) | [A02](01-basics/A02.md) | 26 |
| 4 | [A04 逻辑分支与执行路径](01-basics/A04.md) | [A02](01-basics/A02.md) | 4 |
| 5 | [A05 图像空间变换](01-basics/A05.md) | [A01](01-basics/A01.md)、[A02](01-basics/A02.md) | 17 |
| 6 | [A06 图像颜色与滤波](01-basics/A06.md) | [A01](01-basics/A01.md) | 15 |
| 7 | [A07 遮罩数值与空间范围](01-basics/A07.md) | [A01](01-basics/A01.md)、[A05](01-basics/A05.md) | 13 |
| 8 | [A08 遮罩合成与透明通道](01-basics/A08.md) | [A07](01-basics/A07.md) | 4 |
| 9 | [A09 批次 列表与分块](01-basics/A09.md) | [A05](01-basics/A05.md) | 10 |
| 10 | [A10 边界框与图层](01-basics/A10.md) | [A05](01-basics/A05.md)、[A08](01-basics/A08.md) | 7 |
| 11 | [A11 图像来源与导出格式](01-basics/A11.md) | [A01](01-basics/A01.md)、[A09](01-basics/A09.md) | 7 |
| 12 | [A12 图文数据集配对](01-basics/A12.md) | [A03](01-basics/A03.md)、[A09](01-basics/A09.md) | 6 |
| 13 | [A13 图像着色器](01-basics/A13.md) | [A06](01-basics/A06.md) | 1 |
| 14 | [B01 加载器与最小条件编码](02-generation/B01.md) | [A03](01-basics/A03.md) | 13 |
| 15 | [B02 像素与潜空间往返](02-generation/B02.md) | [B01](02-generation/B01.md)、[A06](01-basics/A06.md) | 4 |
| 16 | [B03 最小文生图与复现](02-generation/B03.md) | [B01](02-generation/B01.md)、[B02](02-generation/B02.md) | 2 |
| 17 | [B04 图生图与去噪强度](02-generation/B04.md) | [B03](02-generation/B03.md) | 1 |
| 18 | [B05 局部重绘与外扩](02-generation/B05.md) | [B04](02-generation/B04.md)、[A07](01-basics/A07.md)、[A08](01-basics/A08.md) | 3 |
| 19 | [B06 潜空间操作与保存](02-generation/B06.md) | [B02](02-generation/B02.md)、[B04](02-generation/B04.md)、[A09](01-basics/A09.md) | 27 |
| 20 | [B07 拆开采样器](02-generation/B07.md) | [B03](02-generation/B03.md) | 9 |
| 21 | [B08 噪声时间表与分段采样](02-generation/B08.md) | [B07](02-generation/B07.md) | 17 |
| 22 | [B09 采样算法的替换](02-generation/B09.md) | [B07](02-generation/B07.md) | 14 |
| 23 | [B10 引导器与引导补丁](02-generation/B10.md) | [B07](02-generation/B07.md) | 21 |
| 24 | [B11 条件组合 区域与时段](02-generation/B11.md) | [B03](02-generation/B03.md)、[A07](01-basics/A07.md) | 12 |
| 25 | [B12 LoRA 与旁路](02-generation/B12.md) | [B03](02-generation/B03.md) | 5 |
| 26 | [B13 ControlNet 与结构条件](02-generation/B13.md) | [B03](02-generation/B03.md)、[A06](01-basics/A06.md) | 8 |
| 27 | [B14 图像编码与风格身份条件](02-generation/B14.md) | [B03](02-generation/B03.md)、[A01](01-basics/A01.md) | 11 |
| 28 | [C01 视频拆分与封装](03-audio-video/C01.md) | [A09](01-basics/A09.md) | 5 |
| 29 | [C02 视频时间裁剪与潜空间帧](03-audio-video/C02.md) | [C01](03-audio-video/C01.md)、[B06](02-generation/B06.md) | 6 |
| 30 | [C03 音频通道 时间与封装](03-audio-video/C03.md) | [C01](03-audio-video/C01.md) | 15 |
| 31 | [C04 学习型放大与插帧](03-audio-video/C04.md) | [A05](01-basics/A05.md)、[C01](03-audio-video/C01.md) | 5 |
| 32 | [C05 视频与图文数据集](03-audio-video/C05.md) | [C02](03-audio-video/C02.md)、[A12](01-basics/A12.md) | 4 |
| 33 | [D01 H3 参考视频最小闭环](04-minimax-h3/D01.md) | [B01](02-generation/B01.md)、[B07](02-generation/B07.md)、[C01](03-audio-video/C01.md)、[C03](03-audio-video/C03.md) | 3 |
| 34 | [D02 H3 首末帧与时长网格](04-minimax-h3/D02.md) | [D01](04-minimax-h3/D01.md) | 2 |
| 35 | [D03 H3 时间锚点与多参考](04-minimax-h3/D03.md) | [D02](04-minimax-h3/D02.md) | 1 |
| 36 | [D04 H3 视频与音频采样偏移](04-minimax-h3/D04.md) | [D01](04-minimax-h3/D01.md)、[B08](02-generation/B08.md) | 1 |
| 37 | [F01 三维文件 相机与预览](06-vision-3d/F01.md) | [A01](01-basics/A01.md)、[C01](03-audio-video/C01.md) | 9 |
| 38 | [F02 图像几何估计与网格](06-vision-3d/F02.md) | [A05](01-basics/A05.md)、[F01](06-vision-3d/F01.md) | 10 |
| 39 | [F03 网格后处理与文件转换](06-vision-3d/F03.md) | [F02](06-vision-3d/F02.md)、[F01](06-vision-3d/F01.md) | 11 |
| 40 | [F04 UV 贴图与烘焙](06-vision-3d/F04.md) | [F03](06-vision-3d/F03.md) | 7 |
| 41 | [F05 Splat 数据 文件与渲染](06-vision-3d/F05.md) | [F01](06-vision-3d/F01.md) | 9 |
| 42 | [F06 目标检测与自动遮罩](06-vision-3d/F06.md) | [A07](01-basics/A07.md)、[A10](01-basics/A10.md) | 4 |
| 43 | [F07 视频目标跟踪](06-vision-3d/F07.md) | [F06](06-vision-3d/F06.md)、[C02](03-audio-video/C02.md) | 3 |
| 44 | [F08 SAM3D 人体姿态预测](06-vision-3d/F08.md) | [C02](03-audio-video/C02.md)、[F06](06-vision-3d/F06.md)、[F01](06-vision-3d/F01.md) | 3 |
| 45 | [F09 姿态时序平滑](06-vision-3d/F09.md) | [F08](06-vision-3d/F08.md) | 1 |
| 46 | [F10 人体动画导出](06-vision-3d/F10.md) | [F09](06-vision-3d/F09.md)、[F01](06-vision-3d/F01.md) | 1 |
| 47 | [F11 人脸关键点与人体表情](06-vision-3d/F11.md) | [F08](06-vision-3d/F08.md) | 5 |
| 48 | [F12 二维姿态与关键点表示](06-vision-3d/F12.md) | [F06](06-vision-3d/F06.md) | 3 |
| 49 | [G01 模型补丁与注意力实验](07-advanced/G01.md) | [B07](02-generation/B07.md)、[B10](02-generation/B10.md) | 30 |
| 50 | [G02 Hook 的时间控制与组合](07-advanced/G02.md) | [B11](02-generation/B11.md)、[B12](02-generation/B12.md) | 19 |
| 51 | [G03 模型合并与保存回读](07-advanced/G03.md) | [B12](02-generation/B12.md) | 30 |
| 52 | [G04 性能 缓存与设备](07-advanced/G04.md) | [B07](02-generation/B07.md) | 9 |
| 53 | [G05 训练数据与最小 LoRA 训练](07-advanced/G05.md) | [A12](01-basics/A12.md)、[B12](02-generation/B12.md) | 6 |
| 54 | [G06 弃用占位节点兼容性](07-advanced/G06.md) | [B03](02-generation/B03.md) | 1 |
| 55 | [E01 SDXL SD3 与 Refiner 条件](05-model-families/E01.md) | [B03](02-generation/B03.md)、[B07](02-generation/B07.md) | 4 |
| 56 | [E02 Flux 与多参考](05-model-families/E02.md) | [B03](02-generation/B03.md)、[B07](02-generation/B07.md) | 8 |
| 57 | [E03 Qwen 图像编辑与分层](05-model-families/E03.md) | [B04](02-generation/B04.md)、[B07](02-generation/B07.md)、[A08](01-basics/A08.md) | 4 |
| 58 | [E04 HiDream 图像与参考条件](05-model-families/E04.md) | [B03](02-generation/B03.md)、[B07](02-generation/B07.md) | 3 |
| 59 | [E05 其他图像家族的编码与编辑](05-model-families/E05.md) | [B04](02-generation/B04.md)、[B07](02-generation/B07.md) | 10 |
| 60 | [E06 多阶段生成与专项图像处理](05-model-families/E06.md) | [B04](02-generation/B04.md)、[B05](02-generation/B05.md)、[B07](02-generation/B07.md) | 9 |
| 61 | [E07 LTX 视频与音频联合潜空间](05-model-families/E07.md) | [B07](02-generation/B07.md)、[C01](03-audio-video/C01.md)、[C03](03-audio-video/C03.md) | 19 |
| 62 | [E08 Hunyuan 视频与超分阶段](05-model-families/E08.md) | [B07](02-generation/B07.md)、[C01](03-audio-video/C01.md)、[C03](03-audio-video/C03.md) | 8 |
| 63 | [E09 Cosmos Kandinsky Mochi 与 SVD 视频](05-model-families/E09.md) | [B07](02-generation/B07.md)、[C01](03-audio-video/C01.md)、[C03](03-audio-video/C03.md) | 8 |
| 64 | [E10 自回归视频采样](05-model-families/E10.md) | [B07](02-generation/B07.md)、[C01](03-audio-video/C01.md)、[C03](03-audio-video/C03.md) | 3 |
| 65 | [E11 Wan 基础与首末帧](05-model-families/E11.md) | [B07](02-generation/B07.md)、[C01](03-audio-video/C01.md)、[C03](03-audio-video/C03.md) | 3 |
| 66 | [E12 Wan 轨迹与相机控制](05-model-families/E12.md) | [E11](05-model-families/E11.md)、[A10](01-basics/A10.md) | 8 |
| 67 | [E13 Wan 遮罩 控制与主体参考](05-model-families/E13.md) | [E11](05-model-families/E11.md)、[B05](02-generation/B05.md)、[F06](06-vision-3d/F06.md) | 6 |
| 68 | [E14 Wan 人体动作与 SCAIL](05-model-families/E14.md) | [E11](05-model-families/E11.md)、[F08](06-vision-3d/F08.md)、[F09](06-vision-3d/F09.md) | 5 |
| 69 | [E15 Wan 音频驱动与续接](05-model-families/E15.md) | [E11](05-model-families/E11.md)、[C03](03-audio-video/C03.md) | 10 |
| 70 | [E16 VOID 视频修补与光流噪声](05-model-families/E16.md) | [C02](03-audio-video/C02.md)、[B05](02-generation/B05.md)、[B07](02-generation/B07.md) | 6 |
| 71 | [E17 Hunyuan 三维生成与体素网格](05-model-families/E17.md) | [B07](02-generation/B07.md)、[B14](02-generation/B14.md)、[F01](06-vision-3d/F01.md) | 6 |
| 72 | [E18 Trellis 与其它三维阶段条件](05-model-families/E18.md) | [B07](02-generation/B07.md)、[F01](06-vision-3d/F01.md) | 10 |
| 73 | [E19 TripoSplat 生成](05-model-families/E19.md) | [B07](02-generation/B07.md)、[F01](06-vision-3d/F01.md) | 4 |
| 74 | [E20 多视角图像与相机条件](05-model-families/E20.md) | [B07](02-generation/B07.md)、[F01](06-vision-3d/F01.md) | 3 |
| 75 | [E21 音频 VAE 与音频生成家族](05-model-families/E21.md) | [B07](02-generation/B07.md)、[C03](03-audio-video/C03.md) | 10 |
| 76 | [E22 SeedVR2 与 SUPIR 修复](05-model-families/E22.md) | [C04](03-audio-video/C04.md)、[B04](02-generation/B04.md) | 6 |
| 77 | [E23 语言生成与专用提示词](05-model-families/E23.md) | [A03](01-basics/A03.md)、[B01](02-generation/B01.md) | 3 |
| 78 | [E24 扩展模型补丁加载](05-model-families/E24.md) | [B12](02-generation/B12.md)、[G01](07-advanced/G01.md) | 3 |
