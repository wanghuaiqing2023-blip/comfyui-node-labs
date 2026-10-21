# ModelMergeCosmos14B：可观察实验

[所属实验 G03](../../labs/07-advanced/G03.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

准备相同架构、相同参数key/shape的A/B；最好A与B只有一组已知非零权重差，禁止原地覆盖源模型。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| G03/ModelMergeCosmos14B/01 | A与A执行本节点 | 加法类预期对应权重加倍；减法类在multiplier=1时对应权重为0；插值/分块类A与A应恢复A。按本节点运算分类核对，不能统一判“像原模型”。 | 读取可合并权重的小样本，不把生成图相似当权重公式证据。 |
| G03/ModelMergeCosmos14B/02 | 仅改变一个权重控制：pos_embedder. | 该控制对应参数组的合并系数改变，未选组保持其原系数。对于分块混合，逐组重复0/0.5/1扫描；单组测试不能代替其它组。 | 记录权重key、输入值和结果值；端点方向先以A/B已知差分确认；不存在的层单列不适用。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| model1 | MODEL | required | — |
| model2 | MODEL | required | — |
| pos_embedder. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| extra_pos_embedder. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| x_embedder. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| t_embedder. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| affline_norm. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block0. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block1. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block2. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block3. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block4. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block5. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block6. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block7. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block8. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block9. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block10. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block11. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block12. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block13. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block14. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block15. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block16. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block17. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block18. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block19. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block20. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block21. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block22. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block23. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block24. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block25. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block26. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block27. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block28. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block29. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block30. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block31. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block32. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block33. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block34. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
| blocks.block35. | FLOAT | required | 默认 1.0；最小 0.0；最大 1.0；步长 0.01 |
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
