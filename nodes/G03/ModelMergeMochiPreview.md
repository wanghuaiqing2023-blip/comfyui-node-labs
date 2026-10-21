# ModelMergeMochiPreview：可观察实验

[所属实验 G03](../../labs/07-advanced/G03.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 节点作用与常见使用场景

**主要作用：按 Mochi 层结构合并权重。**

- 研究同架构权重组合并保存可回读结果时，用于按 Mochi 层结构合并权重。

## 前置节点与输入依赖

“必需”指本节点需要该输入，不表示必须使用表中的某个指定节点。多个来源通常是替代方案；可选输入只在相应场景接入。来源列给出节点页面与输出端口，便于先做上游实验。

**依据边界：** 基于固定索引的端口契约和场景整理，未逐条实测接线。模型、条件和潜变量的来源明确标为兼容性候选；动态端口必须展开核对。详见[依赖标记说明](../../guides/node-page-contract.md)。

| 本节点输入 | 必需性 | 前置节点 → 输出端口 / 输入来源 | 条件与限制 |
|---|---|---|---|
| `model1` / `MODEL` | 必需 | [UNETLoader](../B01/UNETLoader.md) → `MODEL`（兼容性候选）；[CheckpointLoaderSimple](../B01/CheckpointLoaderSimple.md) → `MODEL`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |
| `model2` / `MODEL` | 必需 | [UNETLoader](../B01/UNETLoader.md) → `MODEL`（兼容性候选）；[CheckpointLoaderSimple](../B01/CheckpointLoaderSimple.md) → `MODEL`（兼容性候选） | 接口来源示例，可选其一或使用等价上游；不是要求全部连接。 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。 |

**文本、数值与选项输入：** `pos_frequencies.`、`t_embedder.`、`t5_y_embedder.`、`t5_yproj.`、`blocks.0.`、`blocks.1.`、`blocks.2.`、`blocks.3.`、`blocks.4.`、`blocks.5.`、`blocks.6.`、`blocks.7.`、`blocks.8.`、`blocks.9.`、`blocks.10.`、`blocks.11.`、`blocks.12.`、`blocks.13.`、`blocks.14.`、`blocks.15.`、`blocks.16.`、`blocks.17.`、`blocks.18.`、`blocks.19.`、`blocks.20.`、`blocks.21.`、`blocks.22.`、`blocks.23.`、`blocks.24.`、`blocks.25.`、`blocks.26.`、`blocks.27.`、`blocks.28.`、`blocks.29.`、`blocks.30.`、`blocks.31.`、`blocks.32.`、`blocks.33.`、`blocks.34.`、`blocks.35.`、`blocks.36.`、`blocks.37.`、`blocks.38.`、`blocks.39.`、`blocks.40.`、`blocks.41.`、`blocks.42.`、`blocks.43.`、`blocks.44.`、`blocks.45.`、`blocks.46.`、`blocks.47.`、`final_layer.`。按实际界面填写；若端口要求连线或支持“转为输入”，可连接同类型数据源。它们不自动构成必须先学习 Primitive 节点的依赖。默认值见下方输入清单。

### 建议先学哪些节点

先学习本次所选输入来源对应的节点：[UNETLoader](../B01/UNETLoader.md)、[CheckpointLoaderSimple](../B01/CheckpointLoaderSimple.md)。只选择当前分支需要的来源，不要求全部完成。

学习顺序与运行依赖分开：所属实验组负责能力安排，上表负责本节点输入；节点可以重复用于多个流程，因此这些来源示例不是全局无环拓扑，也不允许把同一实例输出接回自身。

## 基准与接线

准备相同架构、相同参数key/shape的A/B；最好A与B只有一组已知非零权重差，禁止原地覆盖源模型。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| G03/ModelMergeMochiPreview/01 | A与A执行本节点 | 加法类预期对应权重加倍；减法类在multiplier=1时对应权重为0；插值/分块类A与A应恢复A。按本节点运算分类核对，不能统一判“像原模型”。 | 读取可合并权重的小样本，不把生成图相似当权重公式证据。 |
| G03/ModelMergeMochiPreview/02 | 仅改变一个权重控制：pos_frequencies. | 该控制对应参数组的合并系数改变，未选组保持其原系数。对于分块混合，逐组重复0/0.5/1扫描；单组测试不能代替其它组。 | 记录权重key、输入值和结果值；端点方向先以A/B已知差分确认；不存在的层单列不适用。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| model1 | MODEL | required | — |
| model2 | MODEL | required | — |
| pos_frequencies. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| t_embedder. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| t5_y_embedder. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| t5_yproj. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.0. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.1. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.2. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.3. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.4. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.5. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.6. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.7. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.8. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.9. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.10. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.11. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.12. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.13. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.14. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.15. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.16. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.17. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.18. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.19. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.20. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.21. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.22. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.23. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.24. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.25. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.26. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.27. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.28. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.29. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.30. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.31. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.32. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.33. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.34. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.35. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.36. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.37. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.38. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.39. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.40. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.41. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.42. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.43. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.44. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.45. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.46. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.47. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| final_layer. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| MODEL | MODEL |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_model_merging_model_specific`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
