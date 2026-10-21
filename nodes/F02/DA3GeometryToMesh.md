# DA3GeometryToMesh：可观察实验

[所属实验 F02](../../labs/06-vision-3d/F02.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

冻结同一geometry；batch_index选0；场景含前后景深度断层。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| F02/DA3GeometryToMesh/01 | decimation提高 | 采样更稀疏，顶点/面数通常减少；依据本机参数含义先确认是步长还是比例。 | 读实际mesh统计；未确认方向前不签收。 |
| F02/DA3GeometryToMesh/02 | 断层过滤由宽松变严格 | 跨前后景的错误连接面应减少；可能增加边界孔洞。 | 放大深度断层处，量边界环与跨层三角形。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| da3_geometry | DA3_GEOMETRY | required | — |
| batch_index | INT | required | 默认 0；最小 0；最大 4096；源码提示：Which image of a batch to convert. Per-image vertex counts differ so batches cannot be stacked. |
| decimation | INT | required | 默认 1；最小 1；最大 8；源码提示：Vertex stride. 1 = full resolution, 2 = half, etc. |
| discontinuity_threshold | FLOAT | required | 默认 0.04；最小 0.0；最大 1.0；步长 0.01；源码提示：Drop triangles whose 3x3 depth span exceeds this fraction. 0 = off. |
| confidence_threshold | FLOAT | required | 默认 0.1；最小 0.0；最大 1.0；步长 0.01；源码提示：Exclude pixels whose per-image normalised confidence is below this value (0 = keep all, 1 = keep only the single most confident pixel). Used when the geometry has a confidence map (Small/Base models). |
| use_sky_mask | BOOLEAN | required | 默认 True；源码提示：Exclude sky-probability pixels (sky &gt;= 0.5) from the mesh. Used when the geometry has a sky map (Mono/Metric models). |
| texture | BOOLEAN | required | 默认 True；源码提示：Use the source image as a base color texture. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| MESH | MESH |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_depth_anything_3`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
