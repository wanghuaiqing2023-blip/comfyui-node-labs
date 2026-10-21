# CLIPTextEncodePixArtAlpha：可观察实验

[所属实验 E05](../../labs/05-model-families/E05.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：编码 PixArtAlpha 文本与尺寸条件。**

- 使用本节点名称所对应的图像模型模板时，用于编码 PixArtAlpha 文本与尺寸条件。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `clip` / `CLIP` | 必需 | [CLIPLoader](../B01/CLIPLoader.md) → `CLIP`（兼容性候选）；[DualCLIPLoader](../B01/DualCLIPLoader.md) → `CLIP`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |

**文本、数值与选项输入：** `width`、`height`、`text`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[CLIPLoader](../B01/CLIPLoader.md)、[DualCLIPLoader](../B01/DualCLIPLoader.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

先完成所属实验组的上游闭环，保存一份冻结输入；模型文件、dtype、设备与随机种子都记录到实验表。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| E05/CLIPTextEncodePixArtAlpha/01 | 只把描述red cube on white background改为blue sphere on white background；字段：text | 编码节点：条件embedding/metadata应随文本改变，非直接输出图片；生成文本节点：实际返回文本。下游生成更倾向对应颜色/物体，但不是必然。 | 固定CLIP和模型；记录条件shape/数值摘要，5seed统计对象/颜色/背景三项，不能只改token长度同时换模型。 |
| E05/CLIPTextEncodePixArtAlpha/02 | 恢复原文本，所有采样配置/参考输入保持 | 纯编码同环境应可复现；自回归/音乐/文本生成编码涉及内部随机时还须固定其seed/采样策略。 | 比较输出embedding或文本，记录内部seed是否暴露；没有暴露则标随机而非失败。 |
| E05/CLIPTextEncodePixArtAlpha/03 | 单参数数值扫描：width = 768 → 1024 → 1280（其它保持基准） | 这是本节点的分辨率条件/配置；应改变对应width元数据或计算分布，不等于立即把输入IMAGE缩放。 | 每次记录直接输出shape/对应metadata；取整规则未知时先核对模型配置，不能套用SD的8倍。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| width | INT | required | 默认 1024；最小 0；最大 16384 |
| height | INT | required | 默认 1024；最小 0；最大 16384 |
| text | STRING | required | 多行文本 |
| clip | CLIP | required | — |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| CONDITIONING | CONDITIONING |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_pixart`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
