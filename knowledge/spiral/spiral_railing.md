# Procedural Spiral Staircase — Railing / 螺旋楼梯扶手

## Retrieval metadata

Type: Example + Pattern
Asset: Staircase
Variant: Spiral
Module: RAIL

## Purpose

Add a procedural handrail that follows the spiral staircase transform and is controlled by railing parameters.

## Relevant user requests

- Add a railing to a spiral staircase.
- Create a spiral handrail.
- Create stairs with railings.
- 给螺旋楼梯添加扶手。
- 创建螺旋扶手。

## Relationship to the full example

This chunk is extracted from the verified full spiral-staircase example. It is intended as a RAG retrieval unit, not as a standalone replacement for the archived full script.


## Railing pattern

Start point
→ Start transform
→ Copy anchors using the STEP-copy transform
→ Copy vertical rail guides to anchor points
→ Select start vertices
→ Build path
→ Resample
→ Sweep main rail
→ Build secondary rail
→ Merge rails

## Railing parameters

- `railHeight`
- `railSize`

## Dependency

This chunk depends on the core staircase chunk, especially `Controller` and `STEP_copy`.

## Verified source excerpt

```python
# RAIL nodes
n_RAIL_anchor_copy = geo.createNode('copyxform', 'RAIL_anchor_copy')
n_RAIL_anchor_topts = geo.createNode('copytopoints::2.0', 'RAIL_anchor_topts')
n_RAIL_keep_start = geo.createNode('blast', 'RAIL_keep_start')
n_RAIL_main_bevel = geo.createNode('polybevel::3.0', 'RAIL_main_bevel')
n_RAIL_main_cap = geo.createNode('polyextrude::2.0', 'RAIL_main_cap')
n_RAIL_main_tube = geo.createNode('sweep::2.0', 'RAIL_main_tube')
n_RAIL_merge = geo.createNode('merge', 'RAIL_merge')
n_RAIL_path = geo.createNode('add', 'RAIL_path')
n_RAIL_resample = geo.createNode('resample', 'RAIL_resample')
n_RAIL_start_group = geo.createNode('groupexpression', 'RAIL_start_group')
n_RAIL_start_point = geo.createNode('add', 'RAIL_start_point')
n_RAIL_start_xform = geo.createNode('xform', 'RAIL_start_xform')
n_RAIL_sub_tube = geo.createNode('sweep::2.0', 'RAIL_sub_tube')
n_RAIL_vertical = geo.createNode('line', 'RAIL_vertical')

# Controller railing parameters
ctrl = n_Controller
ctrl.addSpareParmTuple(hou.FloatParmTemplate('railHeight', 'Railing Height', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.FloatParmTemplate('railSize', 'Hand Rail Size', 1, default_value=(0.0,)))
ctrl.parm('railHeight').set(4.91)
ctrl.parm('railSize').set(0.2)

# Functional parameters / expressions
p = n_RAIL_anchor_topts.parm('targetattribs')
if p is not None: p.set(3)
p = n_RAIL_start_point.parm('points')
if p is not None: p.set(1)
p = n_RAIL_anchor_copy.parm('sourcegroup')
if p is not None: p.setExpression('chs("../STEP_copy/sourcegroup")')
p = n_RAIL_anchor_copy.parm('sourcegrouptype')
if p is not None: p.setExpression('ch("../STEP_copy/sourcegrouptype")')
p = n_RAIL_anchor_copy.parm('ncy')
if p is not None: p.setExpression('ch("../STEP_copy/ncy")')
p = n_RAIL_anchor_copy.parm('pack')
if p is not None: p.setExpression('ch("../STEP_copy/pack")')
p = n_RAIL_anchor_copy.parm('pivot')
if p is not None: p.setExpression('ch("../STEP_copy/pivot")')
p = n_RAIL_anchor_copy.parm('viewportlod')
if p is not None: p.setExpression('ch("../STEP_copy/viewportlod")')
p = n_RAIL_anchor_copy.parm('xOrd')
if p is not None: p.setExpression('ch("../STEP_copy/xOrd")')
p = n_RAIL_anchor_copy.parm('rOrd')
if p is not None: p.setExpression('ch("../STEP_copy/rOrd")')
p = n_RAIL_anchor_copy.parm('tx')
if p is not None: p.setExpression('ch("../STEP_copy/tx")')
p = n_RAIL_anchor_copy.parm('ty')
if p is not None: p.setExpression('ch("../STEP_copy/ty")')
p = n_RAIL_anchor_copy.parm('tz')
if p is not None: p.setExpression('ch("../STEP_copy/tz")')
p = n_RAIL_anchor_copy.parm('rx')
if p is not None: p.setExpression('ch("../STEP_copy/rx")')
p = n_RAIL_anchor_copy.parm('ry')
if p is not None: p.setExpression('ch("../STEP_copy/ry")')
p = n_RAIL_anchor_copy.parm('rz')
if p is not None: p.setExpression('ch("../STEP_copy/rz")')
p = n_RAIL_anchor_copy.parm('sx')
if p is not None: p.setExpression('ch("../STEP_copy/sx")')
p = n_RAIL_anchor_copy.parm('sy')
if p is not None: p.setExpression('ch("../STEP_copy/sy")')
p = n_RAIL_anchor_copy.parm('sz')
if p is not None: p.setExpression('ch("../STEP_copy/sz")')
p = n_RAIL_anchor_copy.parm('shear1')
if p is not None: p.setExpression('ch("../STEP_copy/shear1")')
p = n_RAIL_anchor_copy.parm('shear2')
if p is not None: p.setExpression('ch("../STEP_copy/shear2")')
p = n_RAIL_anchor_copy.parm('shear3')
if p is not None: p.setExpression('ch("../STEP_copy/shear3")')
p = n_RAIL_anchor_copy.parm('scale')
if p is not None: p.setExpression('ch("../STEP_copy/scale")')
p = n_RAIL_anchor_copy.parm('px')
if p is not None: p.setExpression('ch("../STEP_copy/px")')
p = n_RAIL_anchor_copy.parm('py')
if p is not None: p.setExpression('ch("../STEP_copy/py")')
p = n_RAIL_anchor_copy.parm('pz')
if p is not None: p.setExpression('ch("../STEP_copy/pz")')
p = n_RAIL_anchor_copy.parm('prx')
if p is not None: p.setExpression('ch("../STEP_copy/prx")')
p = n_RAIL_anchor_copy.parm('pry')
if p is not None: p.setExpression('ch("../STEP_copy/pry")')
p = n_RAIL_anchor_copy.parm('prz')
if p is not None: p.setExpression('ch("../STEP_copy/prz")')
p = n_RAIL_anchor_copy.parm('newgroups')
if p is not None: p.setExpression('ch("../STEP_copy/newgroups")')
p = n_RAIL_anchor_copy.parm('newgroupprefix')
if p is not None: p.setExpression('chs("../STEP_copy/newgroupprefix")')
p = n_RAIL_anchor_copy.parm('docopyattrib')
if p is not None: p.setExpression('ch("../STEP_copy/docopyattrib")')
p = n_RAIL_anchor_copy.parm('copyattrib')
if p is not None: p.setExpression('chs("../STEP_copy/copyattrib")')
p = n_RAIL_anchor_topts.parm('applyattribs1')
if p is not None: p.set('*,^v,^Alpha,^N,^up,^pscale,^scale,^orient,^rot,^pivot,^trans,^transform')
p = n_RAIL_anchor_topts.parm('applymethod2')
if p is not None: p.set(2)
p = n_RAIL_anchor_topts.parm('applyattribs2')
if p is not None: p.set('Alpha')
p = n_RAIL_anchor_topts.parm('applymethod3')
if p is not None: p.set(3)
p = n_RAIL_anchor_topts.parm('applyattribs3')
if p is not None: p.set('v')
p = n_RAIL_keep_start.parm('group')
if p is not None: p.set('startPoints')
p = n_RAIL_main_bevel.parm('offset')
if p is not None: p.set(0.10000000149011612)
p = n_RAIL_main_bevel.parm('profileramp1value')
if p is not None: p.set(0.5)
p = n_RAIL_main_bevel.parm('profileramp1interp')
if p is not None: p.set(2)
p = n_RAIL_main_bevel.parm('profileramp2pos')
if p is not None: p.set(1.0)
p = n_RAIL_main_bevel.parm('profileramp2value')
if p is not None: p.set(0.5)
p = n_RAIL_main_bevel.parm('profileramp2interp')
if p is not None: p.set(2)
p = n_RAIL_main_cap.parm('group')
if p is not None: p.set('endcaps')
p = n_RAIL_main_cap.parm('dist')
if p is not None: p.set(0.691)
p = n_RAIL_main_cap.parm('thicknessramp1value')
if p is not None: p.set(1.0)
p = n_RAIL_main_cap.parm('thicknessramp1interp')
if p is not None: p.set(2)
p = n_RAIL_main_cap.parm('thicknessramp2pos')
if p is not None: p.set(1.0)
p = n_RAIL_main_cap.parm('thicknessramp2value')
if p is not None: p.set(1.0)
p = n_RAIL_main_cap.parm('thicknessramp2interp')
if p is not None: p.set(2)
p = n_RAIL_main_cap.parm('twistramp1value')
if p is not None: p.set(0.5)
p = n_RAIL_main_cap.parm('twistramp1interp')
if p is not None: p.set(2)
p = n_RAIL_main_cap.parm('twistramp2pos')
if p is not None: p.set(1.0)
p = n_RAIL_main_cap.parm('twistramp2value')
if p is not None: p.set(0.5)
p = n_RAIL_main_cap.parm('twistramp2interp')
if p is not None: p.set(2)
p = n_RAIL_main_tube.parm('surfaceshape')
if p is not None: p.set(1)
p = n_RAIL_main_tube.parm('radius')
if p is not None: p.setExpression('ch("../Controller/railSize")')
p = n_RAIL_main_tube.parm('endcaptype')
if p is not None: p.set(1)
p = n_RAIL_main_tube.parm('addendcapsgroup')
if p is not None: p.set(1)
p = n_RAIL_main_tube.parm('scaleramp1value')
if p is not None: p.set(1.0)
p = n_RAIL_main_tube.parm('scaleramp2pos')
if p is not None: p.set(1.0)
p = n_RAIL_main_tube.parm('scaleramp2value')
if p is not None: p.set(1.0)
p = n_RAIL_path.parm('stdswitcher1')
if p is not None: p.set(1)
p = n_RAIL_path.parm('switcher1')
if p is not None: p.set(1)
p = n_RAIL_resample.parm('length')
if p is not None: p.set(0.3)
p = n_RAIL_resample.parm('treatpolysas')
if p is not None: p.set(2)
p = n_RAIL_start_group.parm('grouptype')
if p is not None: p.set(1)
p = n_RAIL_start_group.parm('groupname1')
if p is not None: p.set('startPoints')
p = n_RAIL_start_group.parm('snippet1')
if p is not None: p.set('vertexprimindex(0, @vtxnum)==0')
p = n_RAIL_start_point.parm('pt0x')
if p is not None: p.setExpression('ch("../Controller/stepLen") - ch("../Controller/stepLen")/50')
p = n_RAIL_start_xform.parm('ry')
if p is not None: p.setExpression('-ch("../STEP_copy/ry")/2')
p = n_RAIL_sub_tube.parm('surfaceshape')
if p is not None: p.set(1)
p = n_RAIL_sub_tube.parm('radius')
if p is not None: p.setExpression('ch("../Controller/railSize")/1.4')
p = n_RAIL_sub_tube.parm('scaleramp1value')
if p is not None: p.set(1.0)
p = n_RAIL_sub_tube.parm('scaleramp2pos')
if p is not None: p.set(1.0)
p = n_RAIL_sub_tube.parm('scaleramp2value')
if p is not None: p.set(1.0)
p = n_RAIL_vertical.parm('dist')
if p is not None: p.setExpression('ch("../Controller/railHeight")')

# Connections
n_OUT_staircase.setInput(1, n_RAIL_merge)
n_RAIL_anchor_copy.setInput(0, n_RAIL_start_xform)
n_RAIL_anchor_topts.setInput(0, n_RAIL_vertical)
n_RAIL_anchor_topts.setInput(1, n_RAIL_anchor_copy)
n_RAIL_keep_start.setInput(0, n_RAIL_start_group)
n_RAIL_main_bevel.setInput(0, n_RAIL_main_cap)
n_RAIL_main_cap.setInput(0, n_RAIL_main_tube)
n_RAIL_main_tube.setInput(0, n_RAIL_resample)
n_RAIL_merge.setInput(0, n_RAIL_main_bevel)
n_RAIL_merge.setInput(1, n_RAIL_sub_tube)
n_RAIL_path.setInput(0, n_RAIL_keep_start)
n_RAIL_resample.setInput(0, n_RAIL_path)
n_RAIL_start_group.setInput(0, n_RAIL_anchor_topts)
n_RAIL_start_xform.setInput(0, n_RAIL_start_point)
n_RAIL_sub_tube.setInput(0, n_RAIL_anchor_topts)
```
