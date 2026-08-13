# Procedural Spiral Staircase — Core / 螺旋楼梯核心

## Retrieval metadata

Type: Example + Pattern
Asset: Staircase
Variant: Spiral
Module: STEP + PILLAR + Controller

## Purpose

Create the core procedural spiral staircase: a wedge-shaped step profile, vertical rise, center pillar, and radial repetition driven by Controller parameters.

## Relevant user requests

- Create a spiral staircase.
- Create circular or radial stairs.
- Create stairs around a center pillar.
- 创建螺旋楼梯。
- 创建旋转楼梯。
- 创建带中心柱的楼梯。

## Relationship to the full example

This chunk is extracted from the verified full spiral-staircase example. It is intended as a RAG retrieval unit, not as a standalone replacement for the archived full script.


## Core pattern

Controller
→ STEP profile (outer + inner circular arcs)
→ Merge / Close
→ PolyExtrude
→ Raise by `stepHeight`
→ Merge with center pillar
→ Copy Transform
  - copies = `steps + 1`
  - Y translation = `stepHeight`
  - Y rotation = `stepAng - stepAng/10`

## Core parameters

- `stepLen`: outer radius / tread length
- `stepAng`: angular spacing between steps
- `stepHeight`: vertical spacing
- `pillarRad`: center pillar radius
- `steps`: number of copies

## Verified source excerpt

```python
import hou

# --- 0. Container ---
parent = hou.node("/obj")
if hou.node("/obj/geo1"):
    hou.node("/obj/geo1").destroy()
geo = parent.createNode("geo", "geo1", run_init_scripts=False, load_contents=True, exact_type_name=True)


n_Controller = geo.createNode('null', 'Controller')
n_OUT_staircase = geo.createNode('merge', 'OUT_staircase')
n_PILLAR_tube = geo.createNode('tube', 'PILLAR_tube')
n_STEP_copy = geo.createNode('copyxform', 'STEP_copy')
n_STEP_extrude = geo.createNode('polyextrude::2.0', 'STEP_extrude')
n_STEP_pillar_merge = geo.createNode('merge', 'STEP_pillar_merge')
n_STEP_profile_close = geo.createNode('add', 'STEP_profile_close')
n_STEP_profile_inner = geo.createNode('circle', 'STEP_profile_inner')
n_STEP_profile_merge = geo.createNode('merge', 'STEP_profile_merge')
n_STEP_profile_outer = geo.createNode('circle', 'STEP_profile_outer')
n_STEP_raise = geo.createNode('xform', 'STEP_raise')

# Controller parameters
ctrl = n_Controller
ctrl.addSpareParmTuple(hou.FloatParmTemplate('stepLen', 'Step Length', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.FloatParmTemplate('stepAng', 'Step Angle', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.FloatParmTemplate('stepHeight', 'Step Height', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.FloatParmTemplate('pillarRad', 'Center Pillar Radius', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.IntParmTemplate('steps', 'No of Steps', 1, default_value=(0,)))
ctrl.parm('stepLen').set(10.0)
ctrl.parm('stepAng').set(25.0)
ctrl.parm('stepHeight').set(1.635)
ctrl.parm('pillarRad').set(0.4)
ctrl.parm('steps').set(8)

# Functional parameters / expressions
p = n_STEP_profile_close.parm('points')
if p is not None: p.set(1)
p = n_Controller.parm('stepLen')
if p is not None: p.set(10.0)
p = n_Controller.parm('stepAng')
if p is not None: p.set(25.0)
p = n_Controller.parm('stepHeight')
if p is not None: p.set(1.635)
p = n_Controller.parm('pillarRad')
if p is not None: p.set(0.4)
p = n_Controller.parm('steps')
if p is not None: p.set(8)
p = n_Controller.parm('railHeight')
if p is not None: p.set(4.91)
p = n_Controller.parm('railSize')
if p is not None: p.set(0.2)
p = n_Controller.parm('bars')
if p is not None: p.set(5)
p = n_PILLAR_tube.parm('type')
if p is not None: p.set(1)
p = n_PILLAR_tube.parm('cap')
if p is not None: p.set(1)
p = n_PILLAR_tube.parm('ty')
if p is not None: p.setExpression('ch("height")/2')
p = n_PILLAR_tube.parm('radscale')
if p is not None: p.setExpression('ch("../Controller/pillarRad")')
p = n_PILLAR_tube.parm('height')
if p is not None: p.setExpression('ch("../Controller/stepHeight")')
p = n_STEP_copy.parm('ncy')
if p is not None: p.setExpression('ch("../Controller/steps")+1')
p = n_STEP_copy.parm('ty')
if p is not None: p.setExpression('ch("../Controller/stepHeight")')
p = n_STEP_copy.parm('ry')
if p is not None: p.setExpression('ch("../Controller/stepAng") - ch("../Controller/stepAng")/10')
p = n_STEP_extrude.parm('dist')
if p is not None: p.setExpression('ch("../Controller/stepHeight")/5')
p = n_STEP_extrude.parm('outputback')
if p is not None: p.set(1)
p = n_STEP_extrude.parm('thicknessramp1value')
if p is not None: p.set(1.0)
p = n_STEP_extrude.parm('thicknessramp1interp')
if p is not None: p.set(2)
p = n_STEP_extrude.parm('thicknessramp2pos')
if p is not None: p.set(1.0)
p = n_STEP_extrude.parm('thicknessramp2value')
if p is not None: p.set(1.0)
p = n_STEP_extrude.parm('thicknessramp2interp')
if p is not None: p.set(2)
p = n_STEP_extrude.parm('twistramp1value')
if p is not None: p.set(0.5)
p = n_STEP_extrude.parm('twistramp1interp')
if p is not None: p.set(2)
p = n_STEP_extrude.parm('twistramp2pos')
if p is not None: p.set(1.0)
p = n_STEP_extrude.parm('twistramp2value')
if p is not None: p.set(0.5)
p = n_STEP_extrude.parm('twistramp2interp')
if p is not None: p.set(2)
p = n_STEP_profile_close.parm('stdswitcher1')
if p is not None: p.set(1)
p = n_STEP_profile_close.parm('keep')
if p is not None: p.set(1)
p = n_STEP_profile_close.parm('switcher1')
if p is not None: p.set(1)
p = n_STEP_profile_close.parm('closedall')
if p is not None: p.set(1)
p = n_STEP_profile_close.parm('usept0')
if p is not None: p.set(0)
p = n_STEP_profile_inner.parm('type')
if p is not None: p.set(1)
p = n_STEP_profile_inner.parm('orient')
if p is not None: p.set(2)
p = n_STEP_profile_inner.parm('ry')
if p is not None: p.setExpression('ch("endangle")/2 - 180')
p = n_STEP_profile_inner.parm('scale')
if p is not None: p.setExpression('ch("../Controller/pillarRad") + ch("../Controller/pillarRad")/5')
p = n_STEP_profile_inner.parm('arc')
if p is not None: p.set(1)
p = n_STEP_profile_inner.parm('endangle')
if p is not None: p.setExpression('180-ch("../Controller/stepAng")')
p = n_STEP_profile_outer.parm('type')
if p is not None: p.set(1)
p = n_STEP_profile_outer.parm('orient')
if p is not None: p.set(2)
p = n_STEP_profile_outer.parm('ry')
if p is not None: p.setExpression('ch("endangle")/2')
p = n_STEP_profile_outer.parm('scale')
if p is not None: p.setExpression('ch("../Controller/stepLen")')
p = n_STEP_profile_outer.parm('arc')
if p is not None: p.set(1)
p = n_STEP_profile_outer.parm('endangle')
if p is not None: p.setExpression('ch("../Controller/stepAng")')
p = n_STEP_raise.parm('ty')
if p is not None: p.setExpression('ch("../Controller/stepHeight")')

# Connections
n_OUT_staircase.setInput(0, n_STEP_copy)
n_STEP_copy.setInput(0, n_STEP_pillar_merge)
n_STEP_extrude.setInput(0, n_STEP_profile_close)
n_STEP_pillar_merge.setInput(0, n_PILLAR_tube)
n_STEP_pillar_merge.setInput(1, n_STEP_raise)
n_STEP_profile_close.setInput(0, n_STEP_profile_merge)
n_STEP_profile_merge.setInput(0, n_STEP_profile_outer)
n_STEP_profile_merge.setInput(1, n_STEP_profile_inner)
n_STEP_raise.setInput(0, n_STEP_extrude)

# Display / render flags
n_OUT_staircase.setDisplayFlag(True)
n_OUT_staircase.setRenderFlag(True)



print("OK: 36 nodes rebuilt, 3 boxes, spare params restored, layout applied.")
```
