# 更新实验内容

实验方案、运行证据和功能结论分开记录。新实验应写明前置、素材、唯一变量和观察标准；只有真实运行后才修改验证状态。

更新实验或节点分配时，同步修改对应页面、分类目录及 data/ 下的结构化数据。不要根据端口类型自动断言不同模型家族兼容。保留已弃用节点的兼容说明。

运行结构检查：

```bash
python3 tools/validate.py
```

该检查只验证覆盖、依赖与链接，不执行 ComfyUI，不验证模型效果。
# 逐节点用例维护

行为用例在 `tools/lab_cases.py` 中维护；模型家族共性规则和渲染位于 `tools/build_node_labs.py`。修改后运行：

```bash
python3 tools/build_node_labs.py
python3 tools/validate.py
```

不要只改生成的 `nodes/` 页面而不改规则源。新增预期必须注明确定性公式、接口契约、统计倾向或待核对分支；不能把结构校验通过写成模型实验通过。`data/node-schemas.json` 是用户固定索引的解析快照；更新接口时应连同来源commit和版本差异一起审查。
