# 能力阶段与通关标准

[项目首页](../README.md) · [阅读指南](README.md)

| 阶段 | 实验组 | 要形成的能力 | 通关任务 |
|---|---|---|---|
| 0 画布与编辑信息 | [U01—U04](../labs/00-frontend/README.md) | 整理连线、写注释、分组及保存恢复 | 独立整理读图工作流，证明输出不变，并恢复其 UI 备份 |
| 1 可观察的数据流 | [A01](../labs/01-basics/A01.md)—[A04](../labs/01-basics/A04.md) | 分清输入值、对象和输出节点，按端口追踪 | 不看答案搭一个数字运算与文本开关 |
| 2 像素与区域 | [A05](../labs/01-basics/A05.md)—[A13](../labs/01-basics/A13.md) | 操作图像、遮罩、批次和图层 | 换一张图，独立完成局部合成并解释黑白方向 |
| 3 生成最小闭环 | [B01](../labs/02-generation/B01.md)—[B06](../labs/02-generation/B06.md) | 理解模型、条件、latent、VAE 的分工 | 从空 latent 与编码图像分别生成，指出唯一变化 |
| 4 采样与约束 | [B07](../labs/02-generation/B07.md)—[B14](../labs/02-generation/B14.md) | 拆解噪声、引导器、算法、时间表和控制条件 | 重搭模块化采样，解释 5 个入口 |
| 5 时间与声音 | [C01](../labs/03-audio-video/C01.md)—[C05](../labs/03-audio-video/C05.md) | 分清帧数、FPS、时长、音轨和采样率 | 24 帧按 12/24 FPS 导出并正确预测时长 |
| 6 目标模型 | [D01](../labs/04-minimax-h3/D01.md)—[D04](../labs/04-minimax-h3/D04.md)，按需选 E | 使用匹配模板做最小改变，识别专用接口 | 独立改 H3 参考图并完成声音与画面的输出检查 |
| 7 感知与三维 | [F01](../labs/06-vision-3d/F01.md)—[F12](../labs/06-vision-3d/F12.md)，相关 E 组 | 区分检测、姿态、网格、文件与渲染 | 从短视频得到可播放 GLB，解释预测与导出的边界 |
| 8 系统扩展 | [G01](../labs/07-advanced/G01.md)—[G06](../labs/07-advanced/G06.md) | 控制补丁、性能、模型合并和训练变量 | 对一种优化给出速度、资源和误差三方面证据 |

**适合当前目标的主线**：[A01](../labs/01-basics/A01.md)、[A02](../labs/01-basics/A02.md)、[A05](../labs/01-basics/A05.md)、[A07](../labs/01-basics/A07.md)、[A08](../labs/01-basics/A08.md)、[A09](../labs/01-basics/A09.md) → [B01](../labs/02-generation/B01.md)、[B02](../labs/02-generation/B02.md)、[B03](../labs/02-generation/B03.md)、[B07](../labs/02-generation/B07.md) → [C01](../labs/03-audio-video/C01.md)、[C03](../labs/03-audio-video/C03.md) → [D01](../labs/04-minimax-h3/D01.md)—[D04](../labs/04-minimax-h3/D04.md)。[A03](../labs/01-basics/A03.md) 按需要补，[A04](../labs/01-basics/A04.md) 可用于理解 H3 示例的 Turbo 分支。[B03](../labs/02-generation/B03.md) 选已有的轻量图像基线，或通过已跑通模板理解，不要求为了学 H3 下载所有模型。

**BuildPoseFile 主线**：A01/A05/A07 → C01/C02 → F01/F06 → [F08](../labs/06-vision-3d/F08.md) → [F09](../labs/06-vision-3d/F09.md) → [F10](../labs/06-vision-3d/F10.md)。[F07](../labs/06-vision-3d/F07.md) 是多人跟踪分支的前置，不是每个单人导出实验都必须增加的成本。
