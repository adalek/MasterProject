# Procedural Staircase

## Purpose

Create a procedural staircase in Houdini using repeated geometry.

## Knowledge type

Type: Example
Asset: Staircase
Variant: Straight Basic

## Key concepts

- straight staircase
- linear repetition
- box
- Copy to Points
- repeated steps

## Relevant user requests

- Create a staircase.
- Generate procedural stairs.
- Create repeated steps.
- 创建程序化楼梯。
- 创建可调节台阶。

## Recommended node pattern

1. Create one Geometry container under `/obj`.
2. Create one Box SOP as the source step geometry.
3. Create points representing step positions.
4. Use Copy to Points to copy the box onto those points.
5. Set the final node as the display and render node.

## Important Copy to Points connection rule

The source geometry must use input 0.

```python
copy_to_points.setInput(0, box)
```

The target points must use input 1.

```python
copy_to_points.setInput(1, points_node)
```

Do not reverse these inputs.

## Parameter relationships

For step index `i`:

```python
y = i * step_height
z = i * step_depth
```

The overall staircase can expose these controls:

- number of steps
- step width
- step height
- step depth

## Houdini Python example

"""
Houdini 程序化楼梯生成脚本
参数：12 阶，总高 3 米，踏步深 0.3m，宽 1.2m
"""

import hou

def create_procedural_staircase(
    parent_path="/obj",
    geo_name="staircase",
    num_steps=12,
    total_height=3.0,
    step_depth=0.3,
    step_width=1.2
):
    """
    在 Houdini 中创建程序化楼梯

    参数:
        parent_path: 父级网络路径，默认 /obj
        geo_name:    Geometry 容器名称，默认 staircase
        num_steps:   台阶数量，默认 12
        total_height: 总高度（米），默认 3.0
        step_depth:   踏步深度（米），默认 0.3
        step_width:   踏步宽度（米），默认 1.2
    """
    step_height = total_height / num_steps  # 每阶高度

    # ---------- 1. 创建 Geometry 容器 ----------
    obj = hou.node(parent_path)
    geo = obj.createNode("geo", geo_name)
    geo.setComment(f"程序化楼梯 ({num_steps}阶, 总高{total_height}m)")

    # ---------- 2. 单级台阶 (Box) ----------
    box = geo.createNode("box", "single_step")
    box.parmTuple("size").set((step_depth, step_height, step_width))
    # size = (踏步深, 踏步高, 踏步宽)

    # ---------- 3. 生成目标点 (Attribute Wrangle) ----------
    wrangle = geo.createNode("attribwrangle", "step_points")
    wrangle.parm("class").set(0)   # 0 = Detail (只运行一次)

    vex_code = f"""int num_steps = {num_steps};
float total_height = {total_height};
float step_height = total_height / num_steps;
float step_depth = {step_depth};
float step_width = {step_width};

for (int i = 0; i < num_steps; i++) {{
    float x = i * step_depth;
    float y = i * step_height + step_height * 0.5;
    vector pos = set(x, y, 0);
    int pt = addpoint(0, pos);
    vector up = {{0, 1, 0}};
    setpointattrib(0, "up", pt, up);
}}"""
    wrangle.parm("snippet").set(vex_code)

    # ---------- 4. Copy to Points ----------
    copy = geo.createNode("copytopoints", "copy_steps")
    copy.setInput(0, box)       # input0: 要复制的几何体
    copy.setInput(1, wrangle)   # input1: 目标点

    # ---------- 5. 地面 (Grid) ----------
    grid = geo.createNode("grid", "ground")
    grid.parm("orient").set(2)   # ZX Plane (水平面)
    grid.parmTuple("size").set((step_width * 1.8, num_steps * step_depth * 1.2))
    grid.parmTuple("t").set((
        (num_steps - 1) * step_depth * 0.5,
        -0.01,
        0.0
    ))
    grid.parm("rows").set(1)
    grid.parm("cols").set(1)

    # ---------- 6. Merge 输出 ----------
    merge = geo.createNode("merge", "OUT")
    merge.setInput(0, copy)
    merge.setInput(1, grid)
    merge.setDisplayFlag(True)
    merge.setRenderFlag(True)

    # ---------- 7. 布局节点 ----------
    layout_nodes = [box, wrangle, copy, grid, merge]
    for i, node in enumerate(layout_nodes):
        node.setPosition((i * 3.0, 0.0))

    print(f"[完成] 程序化楼梯已创建: {geo.path()}")
    print(f"       - 阶数: {num_steps}")
    print(f"       - 总高: {total_height}m")
    print(f"       - 每阶高: {step_height:.3f}m")
    print(f"       - 踏步深: {step_depth}m")
    print(f"       - 踏步宽: {step_width}m")

    return geo


# ========== 执行 ==========
# Execute immediately inside Houdini.
existing = hou.node("/obj/staircase")

if existing:
    existing.destroy()

create_procedural_staircase()


## Common mistakes

- Creating SOP nodes directly under `/obj`.
- Reversing the Copy to Points inputs.
- Forgetting to set the final display flag.
- Creating geometry directly through `node.geometry()` instead of using SOP nodes.
- Using parameter names without verifying that they exist in the installed Houdini version.