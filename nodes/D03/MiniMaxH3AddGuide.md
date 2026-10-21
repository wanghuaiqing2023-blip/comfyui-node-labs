# MiniMaxH3AddGuide：可观察实验

[所属实验 D03](../../labs/04-minimax-h3/D03.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

已跑通H3链路；保持原始AV latent；positive串过本节点；引导图片用明显不同的红/蓝参考帧。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| D03/MiniMaxH3AddGuide/01 | frame_idx=0 → -1 | 锚点从开头移到末尾；模型生成只预期附近更符合参考，不承诺逐像素复制。 | 按对应帧窗口查看；该节点只输出CONDITIONING，不输出新LATENT。 |
| D03/MiniMaxH3AddGuide/02 | 输入4帧引导 → 5帧 → 22帧 | 按索引：少于5帧只取第一张；5/22为合法片段长度。音频会按剩余时长裁剪。 | 先查条件元数据/源码，再观察生成片段；缺video/audio VAE分别作为条件依赖负例。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| positive | CONDITIONING | required | — |
| latent | LATENT | required | — |
| frame_idx | INT | required | 默认 0；最小 -9999；最大 9999；源码提示：Frame index to anchor the image or the clip's first frame at. Negative values are counted from the end of the video. |
| vae | VAE | optional | 源码提示：Video VAE, needed when an image is connected. |
| audio_vae | VAE | optional | 源码提示：Audio VAE, needed when an audio is connected. |
| image | IMAGE | optional | 源码提示：Image or video frames to anchor. Multi-frame batches are anchored as a clip and cropped down to the model's valid clip lengths: 5, 22, 39... (17k + 5) frames. Batches shorter than 5 frames use only the first image. |
| audio | AUDIO | optional | 源码提示：Soundtrack to anchor starting at the same frame index, cropped to the video's remaining duration. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| positive | CONDITIONING |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_minimax_h3`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
