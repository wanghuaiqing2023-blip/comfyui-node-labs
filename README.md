# ComfyUI 节点依赖实验室

通过可重复的小实验，理解节点的输入、处理、输出及上下游依赖。内容按目录拆分，每个实验组单独一页，便于学习、修订和记录结果。

**78 个后端实验组 · 639 个节点，另有 4 组前端画布实验（18 个用例） · 后端基于索引声明的 ComfyUI 0.33.0。** 当前为实验设计，未在用户环境中运行；设计覆盖不等于实测通过。范围不含第三方节点与云端 API 节点。

## 从这里开始

首次使用画布，先完成 [前端与画布操作实验 U01—U04](labs/00-frontend/README.md)：重路由、注释、分组、保存与恢复。附 RunningHub 环境核对和明确验收标准，当前尚未在平台实测。

1. [第一轮八个练习](quickstart/README.md)：从读取图片、遮罩合成到拆解采样器。
2. [学习路线与阶段目标](guides/learning-path.md)：按能力递进，按目标选分支。
3. [实验操作方法](guides/experiment-method.md)：先预测，再对照，最后换素材复做。
4. [全部实验目录](labs/README.md)：查找前置实验和实验组。
5. [节点索引](node-index/README.md)：从内部类名定位实验。
6. [逐节点实验卡](nodes/README.md)：每个节点的常见使用场景、前置节点、基准输入、预期结果和参数对照。

## 一节点一页：场景、依赖与实验

639 个后端节点，以及 Reroute、Note、Group 三个前端对象，均有独立主实验页面。页面按输入列出前置节点与输出端口链接，区分必需、可选、控件、动态输入和兼容性候选。详见[页面与依赖规范](guides/node-page-contract.md)。

## 怎样验证参数改变后的结果

639 个节点均有独立实验卡，共1473个用例；原来的78个实验组负责学习顺序。先读[测量与判定规则](guides/observable-results.md)，再从节点卡执行单变量对照；使用[单节点记录模板](templates/node-experiment-record.md)保存预测和实测。

可以先看三个示例：[亮度的逐像素公式](nodes/A06/AdjustBrightness.md)、[遮罩阈值与等号边界](nodes/A07/ThresholdMask.md)、[人体动画FPS、位移、轨迹与格式](nodes/F10/BuildPoseFile.md)。基础素材可由 `tools/make_fixtures.py` 生成，图片/PCM音频可用 `tools/measure.py` 测量。

**边界**：全部卡片都是未运行的实验设计；模型家族共性用例不等于逐函数审计，动态子参数与明确标注的探索分支仍需本机核对。[依据与版本差异](guides/expectation-sources.md)列出已核对公式，避免把假设写成实测结果。

## 分类目录

| 目录 | 内容 | 实验组 |
|---|---|---|
| [labs/00-frontend](labs/00-frontend/README.md) | 前端与画布操作（RunningHub / ComfyUI） | U01—U04，4 组 |
| [labs/01-basics](labs/01-basics/README.md) | 图像与数据基础 | A01—A13，13 组 |
| [labs/02-generation](labs/02-generation/README.md) | 模型与生成采样 | B01—B14，14 组 |
| [labs/03-audio-video](labs/03-audio-video/README.md) | 视频与音频 | C01—C05，5 组 |
| [labs/04-minimax-h3](labs/04-minimax-h3/README.md) | MiniMax H3 专项 | D01—D04，4 组 |
| [labs/05-model-families](labs/05-model-families/README.md) | 其他模型家族 | E01—E24，24 组 |
| [labs/06-vision-3d](labs/06-vision-3d/README.md) | 视觉感知与三维 | F01—F12，12 组 |
| [labs/07-advanced](labs/07-advanced/README.md) | 补丁优化与训练 | G01—G06，6 组 |

## 两条优先路线

- **H3 视频路线**：图像与遮罩 → VAE 与采样 → 视频与音频 → [H3 专项](labs/04-minimax-h3/README.md)。接线见 [H3 关键端口](guides/h3-connections.md)。
- **人体动画路线**：视频拆帧 → 检测与姿态预测 → 平滑 → [F10 动画导出](labs/06-vision-3d/F10.md)。完整依赖见 [BuildPoseFile 路线](guides/pose-export.md)。

模型家族专项互为分支，不要求全部做完才进入 H3。相同 MODEL、LATENT 或 CONDITIONING 类型也可能不兼容。

## 辅助资料

- [测试素材要求](guides/fixtures.md)
- [输入来源缺口与条件限制](guides/input-gaps.md)
- [来源与版本边界](guides/sources.md)
- [实验记录模板](templates/experiment-record.md)与[记录目录](records/README.md)
- [工作流目录](workflows/README.md)与[素材目录](assets/README.md)
- [结构化节点与实验数据](data/README.md)
- [维护说明](CONTRIBUTING.md)

## 项目检查

```bash
python3 tools/validate.py
```

检查节点无遗漏、实验依赖无循环、目录链接有效。模型推理需在自己的 ComfyUI 环境中另行执行。
