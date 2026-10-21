# AudioEqualizer3Band：可观察实验

[所属实验 C03](../../labs/03-audio-video/C03.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：调整低中高三个频段。**

- 处理对白、背景音乐或生成音轨时，用于调整低中高三个频段。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `audio` / `AUDIO` | 必需 | [LoadAudio](../C03/LoadAudio.md) → `AUDIO` | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 |

**文本、数值与选项输入：** `low_gain_dB`、`low_freq`、`mid_gain_dB`、`mid_freq`、`mid_q`、`high_gain_dB`、`high_freq`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[LoadAudio](../C03/LoadAudio.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

含低/中/高三个频率的低幅度混合音；所有 gain=0。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| C03/AudioEqualizer3Band/01 | 仅 mid_gain_dB=0 → +6；中心频率对准中频 | 中频附近能量提高，远离频段的分量变化较小；不是全带等比例增益。 | 比较频谱，保留滤波过渡带。 |
| C03/AudioEqualizer3Band/02 | 恢复全部 gain=0 | 应恢复基准频谱/波形（允许滤波数值误差）。 | 记录峰值，避免削波。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| audio | AUDIO | required | — |
| low_gain_dB | FLOAT | required | 默认 0.0；最小 -24.0；最大 24.0；步长 0.1；源码提示：Gain for Low frequencies (Bass) |
| low_freq | INT | required | 默认 100；最小 20；最大 500；源码提示：Cutoff frequency for Low shelf |
| mid_gain_dB | FLOAT | required | 默认 0.0；最小 -24.0；最大 24.0；步长 0.1；源码提示：Gain for Mid frequencies |
| mid_freq | INT | required | 默认 1000；最小 200；最大 4000；源码提示：Center frequency for Mids |
| mid_q | FLOAT | required | 默认 0.707；最小 0.1；最大 10.0；步长 0.1；源码提示：Q factor (bandwidth) for Mids |
| high_gain_dB | FLOAT | required | 默认 0.0；最小 -24.0；最大 24.0；步长 0.1；源码提示：Gain for High frequencies (Treble) |
| high_freq | INT | required | 默认 5000；最小 1000；最大 15000；源码提示：Cutoff frequency for High shelf |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| AUDIO | AUDIO |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_audio`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
