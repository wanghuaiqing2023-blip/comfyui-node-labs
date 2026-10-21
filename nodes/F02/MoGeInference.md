# MoGeInference：可观察实验

[所属实验 F02](../../labs/06-vision-3d/F02.md) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)

**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。

## 基准与接线

固定带前景物与远处背景的照片；全景版本必须使用等距柱状全景。

先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。

## 可观察的预期与参数对照

| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |
|---|---|---|---|
| F02/MoGeInference/01 | 推理后接对应Render与Mesh转换 | 输出有限的几何数据；前景/背景应有可区分深度。不能未经标定宣称绝对米制深度准确。 | 记录有效像素比例、深度范围、重建边界；全景检查接缝。 |
| F02/MoGeInference/02 | resolution/resolution_level升一档 | 细节采样和耗时/显存可能增加；遮挡处仍可能不可靠。 | 固定相机与输入，对同一物体边缘检查。 |

## 实际输入清单

此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。

| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |
|---|---|---|---|
| moge_model | MOGE_MODEL | required | — |
| image | IMAGE | required | — |
| resolution_level | INT | required | 默认 9；最小 0；最大 9；源码提示：0 = fastest, 9 = most detail. |
| fov_x_degrees | FLOAT | required | 默认 0.0；最小 0.0；最大 170.0；步长 0.1；源码提示：Horizontal field of view of the source camera. Sets the focal length used to unproject the depth map into 3D. 0 = auto-recover from the predicted points. |
| batch_size | INT | required | 默认 4；最小 1；最大 64；源码提示：Images per inference call. Lower if you OOM on a long video / image set. |
| force_projection | BOOLEAN | required | 默认 True |
| apply_mask | BOOLEAN | required | 默认 True；源码提示：Set masked-out (sky / invalid) pixels to inf in points and depth so meshing culls them. Disable to keep the raw predicted geometry everywhere; the mask is still returned separately. |

## 输出检查点

| 输出端口 | 类型 |
|---|---|
| moge_geometry | MOGE_GEOMETRY |

## 验收与记录

逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。

若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。

复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。

## 依据与版本

- 索引模块：`comfy_extras.nodes_moge`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。
- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。
