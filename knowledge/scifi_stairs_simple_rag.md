# Parameterized SciFi Staircase / 参数化 SciFi 楼梯

## Purpose

Create a straight procedural staircase with editable controls,
railings, base geometry and UVs.

创建带 Controller、扶手、底座和 UV 的参数化直线楼梯。

## Relevant user requests

- Create a staircase with railings.
- Create a parameterized staircase.
- Create stairs with editable controls.
- Create a SciFi staircase.
- Create stairs with UVs.
- 创建带扶手楼梯。
- 创建参数化楼梯。
- 创建带控制器的楼梯。

## Knowledge type

Type: Example
Asset: Staircase
Variant: Straight Parameterized

## Recommended pattern

Linear repetition using Copy Transform.

Box
→ Copy Transform

Line
→ Resample
→ Sweep
→ Railings

Controller
→ ch() parameter references

## Key concepts

- straight staircase
- linear repetition
- copyxform
- Controller
- spare parameters
- railing
- sweep
- UV

## Features

- Editable Controller parameters
- Dual railings
- Base geometry
- UV generation
- Linear staircase



| 参数 | 默认 | 说明 |
| --- | --- | --- |
| steps | 8 | 台阶数量 |
| stepHeight | 0.25 | 每级高度 |
| stepDepth | 0.4 | 每级深度 |
| stairWidth | 2.0 | 楼梯总宽 |
| railHeight | 0.9 | 扶手高出顶部 |
| railRadius | 0.06 | 扶手管半径 |
| baseHeight | 0.2 | 底座厚 |
| basePad | 0.3 | 底座外扩 |
| F_uv_stretch | 1.0 | UV 密度倍率 |



## Houdini Python example

```python
# ============================================================
# Procedural SciFi Staircase - SIMPLIFIED Version (v1.4)
# ============================================================
# [ASCII-ONLY] English comments; works under ANY encoding.
#
# === ORIGIN ===
# Extracted from official SideFX "SciFi Stairs" tutorial HDA
# (Stair_tool, 107 nodes). Keeps ONLY the core building logic.
# No Labs dependency.
#
# === CORE LOGIC (official -> simplified) ===
#  steps: box(step) + copyxform(N copies)
#  base:  box with padding
#  rails: line(slope) + resample + sweep(round) + xform(right)
#
# === UV (ALL faces, reference to original) ===
#  original: foreach + texture projection + bins + uvtransform
#  simple:   VEX per-face planar UV by face normal:
#            - every face gets its own 0-1 UV (top/sides/front)
#            - aspect-correct (checker stays square per face)
#            - density scaled by F_uv_stretch
#            rails: sweep computeuvs + lengthweighteduvs
#            Check_UV: uvquickshade checkerboard preview
#
# === KEY LESSONS ===
#  - box has NO uv attribute, NO normal intrinsic: face normal
#    must be computed from vertex cross product in VEX
#  - addvertexattrib(geo, name, default) - no size arg!
#  - sweep needs surfaceshape=1 for auto circle cross-section
#  - resample needs dolength=0 + dosegs=1 for full coverage
#  - line has no tx: horizontal offset uses originx
#  - spare parms must be created BEFORE ch() expressions
#
# === CONTROLS (Controller spare parms) ===
#  steps       stair count              8
#  stepHeight  height per step          0.25
#  stepDepth   depth per step           0.4
#  stairWidth  total width              2.0
#  railHeight  railing height above top 0.9
#  railRadius  railing tube radius      0.06
#  baseHeight  base slab height         0.2
#  basePad     base overhang per side   0.3
#  F_uv_stretch UV density multiplier  1.0
#
# === RUN ===
#  exec(open(r"C:/Users/Xuwen/Downloads/scifi_stairs_simple.py").read())
#  or: hython C:/Users/Xuwen/Downloads/scifi_stairs_simple.py
#
# Creates /obj/StairSimple (deletes existing first).
# ============================================================
import hou

parent = hou.node("/obj")
if hou.node("/obj/StairSimple"):
    hou.node("/obj/StairSimple").destroy()
geo = parent.createNode("geo", "StairSimple", run_init_scripts=False, load_contents=True, exact_type_name=True)
geo.move(hou.Vector2(0, 0))

# --- 1. Controller (Null + spare parms, BEFORE expressions) ---
ctrl = geo.createNode("null", "Controller")
ctrl.setComment("Global controls: all sizes driven by ch() here")
ctrl.addSpareParmTuple(hou.IntParmTemplate("steps", "Step Count", 1, default_value=(8,), min=1, max=60))
ctrl.addSpareParmTuple(hou.FloatParmTemplate("stepHeight", "Step Height", 1, default_value=(0.25,), min=0.05, max=1.0))
ctrl.addSpareParmTuple(hou.FloatParmTemplate("stepDepth", "Step Depth", 1, default_value=(0.4,), min=0.1, max=1.5))
ctrl.addSpareParmTuple(hou.FloatParmTemplate("stairWidth", "Stair Width", 1, default_value=(2.0,), min=0.5, max=10.0))
ctrl.addSpareParmTuple(hou.FloatParmTemplate("railHeight", "Rail Height", 1, default_value=(0.9,), min=0.1, max=3.0))
ctrl.addSpareParmTuple(hou.FloatParmTemplate("railRadius", "Rail Radius", 1, default_value=(0.06,), min=0.01, max=0.3))
ctrl.addSpareParmTuple(hou.FloatParmTemplate("baseHeight", "Base Height", 1, default_value=(0.2,), min=0.0, max=1.0))
ctrl.addSpareParmTuple(hou.FloatParmTemplate("basePad", "Base Overhang", 1, default_value=(0.3,), min=0.0, max=2.0))
ctrl.addSpareParmTuple(hou.FloatParmTemplate("F_uv_stretch", "UV Stretch", 1, default_value=(1.0,), min=0.1, max=5.0))

# Per-face planar UV VEX (run over Primitives): every face gets 0-1 UV,
# aspect-correct (checker square on every face), density by F_uv_stretch.
UV_VEX = """
if (!hasvertexattrib(0, "uv"))
    addvertexattrib(0, "uv", {0.0, 0.0, 0.0});
int verts[] = primvertices(0, @primnum);
vector p0 = point(0, "P", vertexpoint(0, verts[0]));
vector p1 = point(0, "P", vertexpoint(0, verts[1]));
vector p2 = point(0, "P", vertexpoint(0, verts[2]));
vector n = normalize(cross(p1 - p0, p2 - p0));
vector absn = abs(n);
int ax = (absn.x >= absn.y && absn.x >= absn.z) ? 0 : (absn.y >= absn.z ? 1 : 2);
vector ua, va;
if (ax == 0) { ua = set(0,0,1); va = set(0,1,0); }
else if (ax == 1) { ua = set(1,0,0); va = set(0,0,1); }
else { ua = set(1,0,0); va = set(0,1,0); }
float minu = 1e9, maxu = -1e9, minv = 1e9, maxv = -1e9;
for (int vi = 0; vi < len(verts); vi++) {
    vector p = point(0, "P", vertexpoint(0, verts[vi]));
    minu = min(minu, dot(p, ua)); maxu = max(maxu, dot(p, ua));
    minv = min(minv, dot(p, va)); maxv = max(maxv, dot(p, va));
}
float scale = max(maxu - minu, maxv - minv) / ch("../Controller/F_uv_stretch");
if (scale <= 1e-9) scale = 1.0;
for (int i = 0; i < len(verts); i++) {
    vector p = point(0, "P", vertexpoint(0, verts[i]));
    vector uv = set((dot(p, ua) - minu) / scale, (dot(p, va) - minv) / scale, 0.0);
    setvertexattrib(0, "uv", @primnum, i, uv);
}
"""

# --- 2. STEP system: step box -> per-face UV -> spiral copy ---
step_box = geo.createNode("box", "STEP_profile")
step_box.setComment("Single step slab (width x height x depth)")
step_uv = geo.createNode("attribwrangle", "STEP_uv")
step_uv.setComment("Per-face planar UV: every face of the step gets UV")
step_uv.parm("class").set(1)  # run over Primitives
step_uv.parm("snippet").set(UV_VEX)
step_uv.setInput(0, step_box)
step_copy = geo.createNode("copyxform", "STEP_copy")
step_copy.setComment("Copies step N times, rising and stepping back each time")
step_copy.setInput(0, step_uv)

# --- 3. RAIL system: sloped line + resample + sweep tube ---
rail_line = geo.createNode("line", "RAIL_line")
rail_line.setComment("Railing backbone: sloped line from first step to top railing")
rail_resample = geo.createNode("resample", "RAIL_resample")
rail_resample.setComment("Subdivides railing line so sweep gets a smooth tube")
rail_resample.setInput(0, rail_line)
rail_sweep = geo.createNode("sweep", "RAIL_sweep")
rail_sweep.setComment("Left railing tube: auto circle cross-section + tube UV")
rail_sweep.setInput(0, rail_resample)
rail_sweep.parm('surfaceshape').set(1)  # 1 = Circle cross-section (no input1 needed)
rail_sweep.parm('computeuvs').set(1)  # generate UV along tube
rail_sweep.parm('lengthweighteduvs').set(1)  # even UV spacing
rail_right = geo.createNode("xform", "RAIL_right")
rail_right.setComment("Right railing = left railing shifted by stairWidth")
rail_right.setInput(0, rail_sweep)

# --- 4. BASE system: base box -> per-face UV ---
base_box = geo.createNode("box", "BASE_box")
base_box.setComment("Ground base slab, wider than stairs by basePad")
base_uv = geo.createNode("attribwrangle", "BASE_uv")
base_uv.setComment("Per-face planar UV for base slab")
base_uv.parm("class").set(1)
base_uv.parm("snippet").set(UV_VEX)
base_uv.setInput(0, base_box)

# --- 5. OUT ---
out = geo.createNode("merge", "OUT_staircase")
out.setComment("Final merge: steps + left rail + right rail + base")
out.setInput(0, step_copy)
out.setInput(1, rail_sweep)
out.setInput(2, rail_right)
out.setInput(3, base_uv)
check = geo.createNode("uvquickshade", "Check_UV")
check.setComment("Checkerboard preview - verify UV on ALL faces")
check.setInput(0, out)

# --- 6. Expressions (all sizes from Controller) ---
def se(node, parm, expr):
    p = node.parm(parm)
    if p is not None:
        p.setExpression(expr)

se(step_box, 'sizex', 'ch("../Controller/stairWidth")')
se(step_box, 'sizey', 'ch("../Controller/stepHeight")')
se(step_box, 'sizez', 'ch("../Controller/stepDepth")')
se(step_box, 'ty', 'ch("../Controller/stepHeight")/2')
se(step_copy, 'ncy', 'ch("../Controller/steps")')
se(step_copy, 'ty', 'ch("../Controller/stepHeight")')
se(step_copy, 'tz', '-ch("../Controller/stepDepth")')
se(rail_line, 'originx', '-ch("../Controller/stairWidth")/2')
se(rail_line, 'originy', 'ch("../Controller/baseHeight") + ch("../Controller/stepHeight")')
se(rail_line, 'diry', 'ch("../Controller/steps") * ch("../Controller/stepHeight") + ch("../Controller/railHeight") - ch("../Controller/stepHeight")')
se(rail_line, 'dirz', '-ch("../Controller/steps") * ch("../Controller/stepDepth")')
se(rail_line, 'dist', 'sqrt(pow(ch("../Controller/steps") * ch("../Controller/stepHeight") + ch("../Controller/railHeight") - ch("../Controller/stepHeight"), 2) + pow(ch("../Controller/steps") * ch("../Controller/stepDepth"), 2))')
se(rail_resample, 'dolength', '0')
se(rail_resample, 'dosegs', '1')
se(rail_resample, 'segs', '32')
se(rail_sweep, 'radius', 'ch("../Controller/railRadius")')
se(rail_right, 'tx', 'ch("../Controller/stairWidth")')
se(base_box, 'sizex', 'ch("../Controller/stairWidth") + 2 * ch("../Controller/basePad")')
se(base_box, 'sizey', 'ch("../Controller/baseHeight")')
se(base_box, 'sizez', 'ch("../Controller/steps") * ch("../Controller/stepDepth") + 2 * ch("../Controller/basePad")')
se(base_box, 'ty', 'ch("../Controller/baseHeight")/2')

# --- 7. Layout ---
ctrl.setPosition((0.0, 12.0))
step_box.setPosition((0.0, 10.0))
step_uv.setPosition((0.0, 9.25))
step_copy.setPosition((0.0, 8.5))
rail_line.setPosition((6.0, 10.0))
rail_resample.setPosition((6.0, 8.5))
rail_sweep.setPosition((6.0, 7.0))
rail_right.setPosition((8.2, 7.0))
base_box.setPosition((12.0, 10.0))
base_uv.setPosition((12.0, 9.0))
out.setPosition((4.0, 4.0))
check.setPosition((4.0, 2.5))

# --- 8. Display ---
out.setDisplayFlag(True)
out.setRenderFlag(True)

# --- 9. NetworkBox groups ---
b1 = geo.createNetworkBox()
b1.setName("STEP_System")
b1.setComment("Steps: slab + per-face UV + copy")
b1.addNode(step_box)
b1.addNode(step_uv)
b1.addNode(step_copy)
b1.fitAroundContents()
b2 = geo.createNetworkBox()
b2.setName("RAIL_System")
b2.setComment("Railings: sloped line swept into tubes")
b2.addNode(rail_line)
b2.addNode(rail_resample)
b2.addNode(rail_sweep)
b2.addNode(rail_right)
b2.fitAroundContents()
b3 = geo.createNetworkBox()
b3.setName("BASE_OUT")
b3.setComment("Base slab + final merge + checker preview")
b3.addNode(base_box)
b3.addNode(base_uv)
b3.addNode(out)
b3.addNode(check)
b3.fitAroundContents()

geo.layoutChildren()

print("OK: StairSimple rebuilt - 12 nodes, 3 boxes, 9 spare parms, ALL-face UV, no Labs dependency.")

```

---

## 第 3 部分：RAG 检索建议

| 检索意图 | 关键词 | 位置 |
| --- | --- | --- |
| 简化楼梯 | StairSimple / 简化版 / 程序化楼梯 | 1.1-1.6 |
| 全面部 UV | per-face UV / 每个面 UV / 面法线投影 | 1.4 |
| box 无法线 | normal intrinsic / 叉积 / primintrinsic | 1.4 踩坑 |
| addvertexattrib | 签名 / 编译报错 / 无 size 参数 | 1.4 踩坑 |
| 台阶复制 | copyxform / ncy | 1.3-1 |
| 扶手管道 | sweep / surfaceshape / computeuvs | 1.3-3, 1.4 |
| 棋盘格长方形 | UV 纵横比 / aspect / scale 归一化 | 1.4 |
| line 水平定位 | originx / 无 tx | 1.3-2 |
| spare 参数顺序 | bad parameter reference | 1.3-6 |
| 原版 HDA | Stair_tool / 107 节点 | 1.2 |
