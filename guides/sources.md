# 依据与版本边界

[项目首页](../README.md) · [阅读指南](README.md)

- [节点索引原文](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-新手入门/ComfyUI-系统学习手册/节点手册/03-全部内置节点索引.md)，文件 blob SHA：be7fcb86b0dd687ea93554e68b5a803b5d36ab4f。
- [H3 参考工作流 JSON](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/04-电商AI工作流/workflows/ecommerce-minimax-h3-local-ref2va.json)。本手册已据其节点和连线核对 H3 参考条件、采样、双 VAE 解码与封装的结构，未运行其权重。
- 仓库提交：3e2e4c43e778e41a9bc577edd8ee3d25ad095471。此 SHA 是学习仓库版本，不是 ComfyUI 源码提交。
- 索引不包括第三方 custom_nodes、云端/API 节点，也不包括前端 Note/Reroute 等；不能称为所有版本、所有安装环境的全部节点。
- 索引有 24 个带“已弃用”标记的条目。保留它们的兼容性验证位置，新建流程优先使用当前替代节点。
- 动态下拉框和自动扩展输入未在索引中全部展开；运行环境中的界面、object_info 与该版本实现决定实际参数。UI 控件和 hidden 输入不能一律当作待接线的数据口。
- 两处需要特别核对：GetImageSize 的文字说明提到图像直通，但表中只列 width/height/batch_size 三个 INT；本手册从 LoadImage 直接分叉给图像消费者。MiniMaxH3AddGuide 的输出表只有 CONDITIONING，不把它画成 LATENT 的生产者。
- 文件里的预期结果是待检验假设。文档、端口和实测冲突时保留证据，追到本机版本源码，不为迎合预期修改记录。
