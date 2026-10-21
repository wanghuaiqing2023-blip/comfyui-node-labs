# 结构化数据

- [nodes.json](nodes.json)：639 个节点的主实验归属、接口类型摘要、索引标记及验证状态。
- [experiments.json](experiments.json)：78 个实验组及学习前置依赖。
- [source.json](source.json)：来源版本。

前置依赖不等于完整的运行时接线图。动态参数和模型兼容性必须在实际版本核对。
# 逐节点实验数据

- `node-schemas.json`：固定索引解析出的639个节点的逐端口输入/输出、默认值及提示。
- `node-experiments.json`：639张卡、1473个用例；每个用例含change（变量）、expected（预期）、observe（测量）。status统一为not_run。
- design=curated表示按节点/特定操作编写，design=family表示按模型家族机制组织并补入当前端口的数值扫描；二者均不代表已经执行或逐函数审计。

动态组合子参数不在原索引展开范围内，需从本机schema补录；不可把有一行format输入等同于已验证全部编码器分支。
