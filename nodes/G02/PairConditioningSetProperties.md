# PairConditioningSetProperties：可观察实验

[所属实验 G02](../../labs/07-advanced/G02.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

先完成所属实验组的上游闭环，保存一份冻结输入；模型文件、dtype、设备与随机种子都记录到实验表。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| G02/PairConditioningSetProperties/01 | 一个hook/condition → 两个可识别对象 | 组合节点保留对应两组条目，属性节点写入对应mask/时段/强度；原始对象应仍可用于未修改基线。 | 查条目标识和metadata，再采样，不能只检查对象非空。 |
| G02/PairConditioningSetProperties/02 | 只改strength；数值用中性值与默认值，开关用false/true | 相应分支的权重/绑定/时段发生变化；未涉及的条件条目不应被意外移除。源码未明确的重复hook合并优先级单列探索。 | 打印每个hook的生效区间与强度；固定随机噪声做A/B。 |
| G02/PairConditioningSetProperties/03 | 单参数数值扫描：strength = 0.75 → 1 → 1.25（其它保持基准） | 所选模块/条件/补丁的系数改变；具体中性值由节点算法决定。可观察目标是配置/权重增量及固定输入的响应，画质没有通用单调方向。 | 先查strength进入的权重/condition/前向配置；再5seed记录目标属性分数和伪影。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| positive_NEW | CONDITIONING | required | — |
| negative_NEW | CONDITIONING | required | — |
| strength | FLOAT | required | 默认 1.0；最小 0.0；最大 10.0；步长 0.01 |
| set_cond_area | COMBO | required | 选项：'default'、'mask bounds' |
| mask | MASK | optional | — |
| hooks | HOOKS | optional | — |
| timesteps | TIMESTEPS_RANGE | optional | — |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| positive | CONDITIONING |
| negative | CONDITIONING |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_hooks`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
