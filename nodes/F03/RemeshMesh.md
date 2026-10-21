# RemeshMesh：可观察实验

[所属实验 F03](../../labs/06-vision-3d/F03.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

G2，记录bounds、孔洞与连通块；其它参数默认。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| F03/RemeshMesh/01 | resolution=默认 → 默认的下一档更高有效值 | 距离场采样更细，通常保留更多细节且面数/耗时增加；不能保证严格面数关系。 | 对比bounds、薄片是否保留、连通块数和耗时。 |
| F03/RemeshMesh/02 | project_back=false → true | 回投影应使重建表面更贴近原网格；不要求拓扑或顶点索引相同。 | 对齐坐标后测表面距离。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| mesh | MESH | required | — |
| resolution | INT | required | 默认 512；最小 32；最大 2048；源码提示：Voxel grid resolution (output density). 256 ~ 100k faces, 512 ~ 1M. For an exact face count, follow with Decimate Mesh. |
| sign_mode | COMFY_DYNAMICCOMBO_V3 | required | 源码提示：udf: robust to messy/non-manifold input. sdf: clean single surface with QEF (Quadratic Error Function) sharp-feature recovery, but needs consistent winding. |
| band | FLOAT | required | 默认 1.0；最小 0.5；最大 4.0；步长 0.1；源码提示：Narrow-band width in voxel units. In UDF mode also offsets the surface. |
| project_back | FLOAT | required | 默认 0.0；最小 0.0；最大 1.0；步长 0.05；源码提示：Linearly interpolate vertices toward the original surface (0 = pure DC, 1 = snapped). |
| fix_poles | BOOLEAN | required | 默认 False；源码提示：Collapse valence-3 vertex pairs (DC T-junction artifact). |
| smooth_iters | INT | required | 默认 0；最小 0；最大 20；源码提示：Taubin smoothing iterations (0 = off). 2-3 cleans DC staircase-like artifacts; higher over-smooth QEF edges. |
| drop_small_components | FLOAT | required | 默认 0.01；最小 0.0；最大 0.5；步长 0.005；源码提示：Drop components below this fraction of the largest's face count. 0 disables. |
| precluster_max_verts | INT | required | 默认 20000000；最小 0；最大 100000000；源码提示：Cap input vertex count before the field queries, inputs above this are cluster-decimated to it first. Prevents OOM on huge meshes. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| mesh | MESH |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_mesh_postprocess`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
