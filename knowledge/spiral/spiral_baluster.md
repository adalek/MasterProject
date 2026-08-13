# Procedural Spiral Staircase — Baluster / 螺旋楼梯栏杆立柱

## Retrieval metadata

Type: Example + Pattern
Asset: Staircase
Variant: Spiral
Module: BALUSTER

## Purpose

Generate repeated baluster posts for the spiral staircase using resampling, point attributes, Copy to Points, path construction, and Sweep.

## Relevant user requests

- Add balusters to a spiral staircase.
- Add railing posts to stairs.
- Create repeated bars along a spiral railing.
- 给螺旋楼梯添加栏杆立柱。
- 沿扶手生成重复立柱。

## Relationship to the full example

This chunk is extracted from the verified full spiral-staircase example. It is intended as a RAG retrieval unit, not as a standalone replacement for the archived full script.


## Baluster pattern

Vertical line
→ Resample by `bars`
→ Group / Blast
→ Create point-number attribute
→ Copy to railing anchors
→ Build path
→ Resample
→ Sweep
→ Cap / Bevel

## Baluster parameter

- `bars`: number of baluster divisions per section

## Dependency

This chunk depends on the core and railing chunks, especially `RAIL_anchor_copy`.

## Verified source excerpt

```python
# BALUSTER nodes
n_BALUSTER_attrib = geo.createNode('attribcreate::2.0', 'BALUSTER_attrib')
n_BALUSTER_bevel = geo.createNode('polybevel::3.0', 'BALUSTER_bevel')
n_BALUSTER_blast = geo.createNode('blast', 'BALUSTER_blast')
n_BALUSTER_cap = geo.createNode('polyextrude::2.0', 'BALUSTER_cap')
n_BALUSTER_group = geo.createNode('grouprange', 'BALUSTER_group')
n_BALUSTER_path = geo.createNode('add', 'BALUSTER_path')
n_BALUSTER_resample = geo.createNode('resample', 'BALUSTER_resample')
n_BALUSTER_resample2 = geo.createNode('resample', 'BALUSTER_resample2')
n_BALUSTER_topts = geo.createNode('copytopoints::2.0', 'BALUSTER_topts')
n_BALUSTER_tube = geo.createNode('sweep::2.0', 'BALUSTER_tube')
n_BALUSTER_vertical = geo.createNode('line', 'BALUSTER_vertical')

# Controller baluster parameter
ctrl = n_Controller
ctrl.addSpareParmTuple(hou.IntParmTemplate('bars', 'No of Bars', 1, default_value=(0,)))
ctrl.parm('bars').set(5)

# Functional parameters / expressions
p = n_BALUSTER_topts.parm('targetattribs')
if p is not None: p.set(3)
p = n_BALUSTER_attrib.parm('name1')
if p is not None: p.set('ptn')
p = n_BALUSTER_attrib.parm('value1v1')
if p is not None: p.setExpression('@ptnum')
p = n_BALUSTER_bevel.parm('offset')
if p is not None: p.set(0.172)
p = n_BALUSTER_bevel.parm('divisions')
if p is not None: p.set(2)
p = n_BALUSTER_bevel.parm('profileramp1value')
if p is not None: p.set(0.5)
p = n_BALUSTER_bevel.parm('profileramp1interp')
if p is not None: p.set(2)
p = n_BALUSTER_bevel.parm('profileramp2pos')
if p is not None: p.set(1.0)
p = n_BALUSTER_bevel.parm('profileramp2value')
if p is not None: p.set(0.5)
p = n_BALUSTER_bevel.parm('profileramp2interp')
if p is not None: p.set(2)
p = n_BALUSTER_blast.parm('group')
if p is not None: p.set('tepPoint')
p = n_BALUSTER_cap.parm('group')
if p is not None: p.set('endcaps')
p = n_BALUSTER_cap.parm('dist')
if p is not None: p.set(0.11)
p = n_BALUSTER_cap.parm('inset')
if p is not None: p.set(0.012)
p = n_BALUSTER_cap.parm('thicknessramp1value')
if p is not None: p.set(1.0)
p = n_BALUSTER_cap.parm('thicknessramp1interp')
if p is not None: p.set(2)
p = n_BALUSTER_cap.parm('thicknessramp2pos')
if p is not None: p.set(1.0)
p = n_BALUSTER_cap.parm('thicknessramp2value')
if p is not None: p.set(1.0)
p = n_BALUSTER_cap.parm('thicknessramp2interp')
if p is not None: p.set(2)
p = n_BALUSTER_cap.parm('twistramp1value')
if p is not None: p.set(0.5)
p = n_BALUSTER_cap.parm('twistramp1interp')
if p is not None: p.set(2)
p = n_BALUSTER_cap.parm('twistramp2pos')
if p is not None: p.set(1.0)
p = n_BALUSTER_cap.parm('twistramp2value')
if p is not None: p.set(0.5)
p = n_BALUSTER_cap.parm('twistramp2interp')
if p is not None: p.set(2)
p = n_BALUSTER_group.parm('groupname1')
if p is not None: p.set('tepPoint')
p = n_BALUSTER_group.parm('grouptype1')
if p is not None: p.set(0)
p = n_BALUSTER_group.parm('end1')
if p is not None: p.set(1)
p = n_BALUSTER_group.parm('invert1')
if p is not None: p.set(1)
p = n_BALUSTER_path.parm('keep')
if p is not None: p.set(1)
p = n_BALUSTER_path.parm('switcher1')
if p is not None: p.set(1)
p = n_BALUSTER_path.parm('add')
if p is not None: p.set(4)
p = n_BALUSTER_path.parm('attrname')
if p is not None: p.set('ptn')
p = n_BALUSTER_resample.parm('dolength')
if p is not None: p.set(0)
p = n_BALUSTER_resample.parm('length')
if p is not None: p.set(0.41)
p = n_BALUSTER_resample.parm('dosegs')
if p is not None: p.set(1)
p = n_BALUSTER_resample.parm('segs')
if p is not None: p.setExpression('ch("../Controller/bars")')
p = n_BALUSTER_resample2.parm('length')
if p is not None: p.set(0.3)
p = n_BALUSTER_resample2.parm('treatpolysas')
if p is not None: p.set(2)
p = n_BALUSTER_topts.parm('applyattribs1')
if p is not None: p.set('*,^v,^Alpha,^N,^up,^pscale,^scale,^orient,^rot,^pivot,^trans,^transform')
p = n_BALUSTER_topts.parm('applymethod2')
if p is not None: p.set(2)
p = n_BALUSTER_topts.parm('applyattribs2')
if p is not None: p.set('Alpha')
p = n_BALUSTER_topts.parm('applymethod3')
if p is not None: p.set(3)
p = n_BALUSTER_topts.parm('applyattribs3')
if p is not None: p.set('v')
p = n_BALUSTER_tube.parm('surfaceshape')
if p is not None: p.set(1)
p = n_BALUSTER_tube.parm('endcaptype')
if p is not None: p.set(1)
p = n_BALUSTER_tube.parm('addendcapsgroup')
if p is not None: p.set(1)
p = n_BALUSTER_tube.parm('scaleramp1value')
if p is not None: p.set(1.0)
p = n_BALUSTER_tube.parm('scaleramp2pos')
if p is not None: p.set(1.0)
p = n_BALUSTER_tube.parm('scaleramp2value')
if p is not None: p.set(1.0)
p = n_BALUSTER_vertical.parm('originy')
if p is not None: p.setExpression('ch("../Controller/stepHeight")')
p = n_BALUSTER_vertical.parm('dist')
if p is not None: p.setExpression('ch("../Controller/railHeight") - ch("../Controller/stepHeight")')

# Connections
n_BALUSTER_attrib.setInput(0, n_BALUSTER_blast)
n_BALUSTER_bevel.setInput(0, n_BALUSTER_cap)
n_BALUSTER_blast.setInput(0, n_BALUSTER_group)
n_BALUSTER_cap.setInput(0, n_BALUSTER_tube)
n_BALUSTER_group.setInput(0, n_BALUSTER_resample)
n_BALUSTER_path.setInput(0, n_BALUSTER_topts)
n_BALUSTER_resample.setInput(0, n_BALUSTER_vertical)
n_BALUSTER_resample2.setInput(0, n_BALUSTER_path)
n_BALUSTER_topts.setInput(0, n_BALUSTER_attrib)
n_BALUSTER_topts.setInput(1, n_RAIL_anchor_copy)
n_BALUSTER_tube.setInput(0, n_BALUSTER_resample2)
n_OUT_staircase.setInput(2, n_BALUSTER_bevel)
```
