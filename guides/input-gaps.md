# 不能仅靠类型表闭合的分支

[项目首页](../README.md) · [阅读指南](README.md)

静态索引能指出接口，但并非每条链都能仅用这 639 个节点构成。以下项目必须先补足证据或输入，不安排为“直接运行即可通过”。

| 情况 | 索引中的证据 | 实验处理 |
|---|---|---|
| SaveSVGNode 的 SVG 输入 | 表内 SVG 输出只来自 SaveSVGNode 自身的直通，未找到独立 SVG 源 | [A11](../labs/01-basics/A11.md) 先标缺 SVG 上游；找到兼容来源或按该版本源码构造测试夹具后再验证保存。不能直接接 STRING 代替 |
| CreateHookKeyframesFromFloats 的 FLOATS | 没有明确声明输出 FLOATS 的节点；CreateList 的输出是动态匹配类型 | [G02](../labs/07-advanced/G02.md) 先核对本机类型规则与实现，不默认 CreateList 或 CurveEditor 能直接连接；其它 keyframe 创建节点可先验证 |
| BuildPoseFile 接受 KIMODO_POSE_DATA | 这份索引未列出 KimodoSample 生产者 | [F10](../labs/06-vision-3d/F10.md) 使用有明确内置上游的 MHR_POSE_DATA；Kimodo 分支标为额外输入依赖 |
| AUDIO_RECORD、WEBCAM、COMPOSITOR、BOUNDING_BOXES、COLORS、LOAD_3D | 部分属于前端交互状态或专用控件，而不是普通上游输出 | 使用节点对应录音、摄像头、画布、调色板或三维视图；不能因找不到同类型输出就断定工作流缺模型 |
| 专用权重和可选依赖 | 注册表记录成功注册，不表示模型已安装、算法后端可用 | 每个模型分支先验证加载与原模板；缺权重/依赖/显存分别记录 |

BuildJsonPromptIdeogram 的 element 明确来自 CreateBoundingBoxes.elements（ARRAY）；即使它被归入文本处理 [A03](../labs/01-basics/A03.md)，这个子实验必须先完成 [A10](../labs/01-basics/A10.md) 的编辑器部分。ImageCropToMask 和 ResizeImageMaskNode 涉及 MASK 的子实验，在 [A07](../labs/01-basics/A07.md) 建立有效遮罩后再回到 [A05](../labs/01-basics/A05.md) 验证。实验组的主归属用于学习管理，不能抹去组内不同节点的真实前置输入。
