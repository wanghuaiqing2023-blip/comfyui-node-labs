# 预期的依据与版本边界

[项目首页](../README.md) · [测量规则](observable-results.md)

接口清单来自用户提供的固定索引commit `3e2e4c43e778e41a9bc577edd8ee3d25ad095471`。它自述ComfyUI 0.33.0，但不能据此断言全部接口等于官方v0.33.0标签。

本次核查官方v0.33.0指向 `2f35f4a08176d993cded35dac3332be4f7287f41`。该提交的 `comfy_extras/nodes_sam3d_body.py` 返回不存在；`nodes_minimax_h3.py`也没有索引中的MiniMaxH3AddGuide。因此这两项的来源边界必须单列。本项目保留用户索引的639节点范围，不把官方标签静默替换成另一套节点集合。

## 已直接核对的确定性行为

| 预期 | 直接核对来源 |
|---|---|
| AdjustBrightness：clamp(x×factor,0,1)；AdjustContrast：clamp((x-0.5)×factor+0.5,0,1)；NormalizeImages：(x-mean)/std | [nodes_dataset.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_dataset.py) |
| ThresholdMask严格大于；FeatherMask从画布边缘做渐变；GrowMask十字或方形邻域 | [nodes_mask.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_mask.py) |
| normal混合=(1-f)A+fB；multiply先逐元素相乘，再按factor混合 | [nodes_post_processing.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_post_processing.py) |
| AudioAdjustVolume：gain=10^(dB/20)，0dB直通 | [nodes_audio.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_audio.py) |
| StringSubstring使用Python[start:end] | [nodes_string.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_string.py) |
| TrimAudioDuration的start_index实际为秒，负值从末尾计；范围裁切并拒绝空区间 | [nodes_audio.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_audio.py) |
| Split输出反alpha遮罩；Join按alpha=1-mask构造RGBA | [nodes_compositing.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_compositing.py) |
| ModelMergeSimple/CLIPMergeSimple系数方向为r×第一对象+(1-r)×第二对象 | [nodes_model_merging.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_model_merging.py)与[add_patches参数定义](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy/model_patcher.py) |
| BasicScheduler低denoise先扩展总步数再截尾；denoise=0返回空数组 | [nodes_custom_sampler.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_custom_sampler.py) |
| H3空AV latent视频/音频为分立张量分支；时间shape由temporal_shape计算 | [nodes_minimax_h3.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_minimax_h3.py) |
| H3参考视频少于5帧报错，按17k+5向下裁；参考标签按类型从1编号，视频音轨按同编号输入配对 | [nodes_minimax_h3.py](https://github.com/Comfy-Org/ComfyUI/blob/2f35f4a08176d993cded35dac3332be4f7287f41/comfy_extras/nodes_minimax_h3.py) |
| BuildPoseFile：MHR的BVH/body_mesh/bones_only有模型依赖；外部_skeleton_override可替代；BVH的-1轨迹落到0；不同GLB表示分支 | [nodes_sam3d_body.py](https://github.com/Comfy-Org/ComfyUI/blob/e638023d54497dbe0579565e5de4bb7076899592/comfy_extras/nodes_sam3d_body.py) |

只列实际核对过的行为，不能把读取一个模块等同于核对其中所有函数。BVH单位与GLB时间数组的端到端行为仍需要检查构建辅助函数并实际导出；卡片的时间/单位关系是明确的验收假设。

## 其余用例的证据等级

1. **接口契约**：端口、默认值、类型、源代码提示由索引支持。参数范围不意味着边界处一定能在现有硬件上运行。
2. **机制推导**：依据代数、几何、编码/解码接口设计的预期；必须用真实实现验证。
3. **统计假设**：模型生成、参考符合度、质量/速度趋势。不承诺严格单调或一定改善。
4. **待核对分支**：枚举未完整列出、动态组合子参数、边界回退、专用模型压缩率、输出缺省值。卡片明确指出需要核对的位置；确认前不能标PASS。

目前所有节点用例均为not_run；没有上传生成图、姿态文件或GPU实验日志作为结果。结构校验仅证明文档和映射完整，不证明这些预期在用户环境中成立。
