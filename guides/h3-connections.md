# H3 关键端口连接表

[项目首页](../README.md) · [阅读指南](README.md)

下表来自已读取的仓库 ref2va JSON；节点名表示类，实例可能不止一个。模型和权重文件按机器现有模板校验，Turbo 开关控制模型与步数时要检查两者一致。

| 上游输出 | 下游输入 | 数据含义 |
|---|---|---|
| CLIPLoader.CLIP | MiniMaxH3ReferenceToVideo.clip | 配套文本/多模态编码器 |
| 视频 VAELoader.VAE | MiniMaxH3ReferenceToVideo.vae 与 VAEDecode.vae | 视频编码与解码 |
| 音频 VAELoader.VAE | MiniMaxH3ReferenceToVideo.audio_vae 与 VAEDecodeAudio.vae | 音频编码与解码 |
| LoadImage.IMAGE | MiniMaxH3ReferenceToVideo.ref_images 的一个展开入口 | 参考图片 |
| MiniMaxH3ReferenceToVideo.positive | BasicGuider.conditioning | 已构造的生成条件 |
| MiniMaxH3ReferenceToVideo.LATENT | SamplerCustomAdvanced.latent_image | 初始联合潜空间 |
| 选定 MODEL | BasicGuider.model，按模板供 scheduler 使用 | 实际参与预测的模型 |
| RandomNoise.NOISE | SamplerCustomAdvanced.noise | 种子控制的噪声来源 |
| BasicGuider.GUIDER | SamplerCustomAdvanced.guider | 引导方式 |
| KSamplerSelect.SAMPLER | SamplerCustomAdvanced.sampler | 采样算法 |
| BasicScheduler.SIGMAS | SamplerCustomAdvanced.sigmas | 噪声时间表 |
| SamplerCustomAdvanced 的 output LATENT | VAEDecode.samples 和 VAEDecodeAudio.samples | 同一联合采样结果进入配套解码分支 |
| VAEDecode.IMAGE | CreateVideo.images | 视频帧 |
| VAEDecodeAudio.AUDIO | CreateVideo.audio | 音轨 |
| CreateVideo.VIDEO | SaveVideo.video | 待保存视频 |

H3 参考实验的先后：先 [D01](../labs/04-minimax-h3/D01.md) 跑通参考条件，再 [D02](../labs/04-minimax-h3/D02.md) 切到匹配的 fl2va 子模板；[D03](../labs/04-minimax-h3/D03.md) 增加锚点；[D04](../labs/04-minimax-h3/D04.md) 才研究 shift。不要在第一轮同时换权重、关 Turbo、改 scheduler 和参考尺寸。
