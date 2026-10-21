# WanContextWindowsManual：可观察实验

[所属实验 G01](../../labs/07-advanced/G01.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：设置 Wan 上下文窗口。**

- 在匹配架构上对比模型运行方式或注意力配置时，用于设置 Wan 上下文窗口。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `model` / `MODEL` | 必需 | [UNETLoader](../B01/UNETLoader.md) → `MODEL`（兼容性候选）；[CheckpointLoaderSimple](../B01/CheckpointLoaderSimple.md) → `MODEL`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |

**文本、数值与选项输入：** `context_length`、`context_overlap`、`context_schedule`、`context_stride`、`closed_loop`、`fuse_method`、`freenoise`、`retain_first_frame`、`split_conds_to_windows`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[UNETLoader](../B01/UNETLoader.md)、[CheckpointLoaderSimple](../B01/CheckpointLoaderSimple.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

先完成所属实验组的上游闭环，保存一份冻结输入；模型文件、dtype、设备与随机种子都记录到实验表。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| G01/WanContextWindowsManual/01 | 原MODEL/CLIP/条件支路与经节点支路对照 | 输出接口保持兼容；补丁本身不产出图片。必须在编码或采样时实际消费才能看到效果。零值是否中性由该算法决定，不能通用设0。 | 保存相同seed的下游结果，记录修改的层/时段/设备配置。 |
| G01/WanContextWindowsManual/02 | 只改context_length：默认值→邻近合法值→恢复默认 | 对应预测/条件/注意力/采样映射改变；最终shape通常保持（下采样/上下文补丁另查中间shape）。效果/速度/质量不保证单调。 | 观察对象中对应配置，并配对5seed记录提示词符合率、伪影、耗时；只看最终图不能证明指定层生效。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| model | MODEL | required | 源码提示：The model to apply context windows to during sampling. |
| context_length | INT | required | 默认 81；最小 1；最大 16384；步长 4；源码提示：The length of the context window in real frames. Must be 4*n + 1. |
| context_overlap | INT | required | 默认 30；最小 0；源码提示：The overlap of the context window in real frames. |
| context_schedule | COMBO | required | 默认 'standard_uniform'；源码提示：Step-dependent scheduling algorithm for context windows. |
| context_stride | INT | required | 默认 1；最小 1；源码提示：The stride of the context window; only applicable to uniform schedules. |
| closed_loop | BOOLEAN | required | 默认 False；源码提示：Whether to close the context window loop; only applicable to looped schedules. |
| fuse_method | COMBO | required | 默认 'pyramid'；源码提示：The method to use to fuse the context windows. |
| freenoise | BOOLEAN | required | 默认 True；源码提示：Whether to apply FreeNoise noise shuffling, improves window blending. |
| retain_first_frame | BOOLEAN | required | 默认 False；源码提示：Retain the first I2V frame in every context window (may help retain initial reference). |
| split_conds_to_windows | BOOLEAN | required | 默认 False；源码提示：Whether to split multiple conditionings (created by ConditionCombine) to each window based on region index. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| MODEL | MODEL |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_context_windows`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
