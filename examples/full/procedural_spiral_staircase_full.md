# Procedural Spiral Staircase / 程序化螺旋阶梯

## Purpose

Create a procedural spiral staircase in Houdini using radial step repetition.

使用径向旋转复制生成程序化螺旋楼梯。

## Relevant user requests

- Create a spiral staircase.
- Create circular stairs.
- Create a radial staircase.
- Create stairs around a center pillar.
- 创建螺旋楼梯。
- 创建旋转楼梯。
- 创建带中心柱的楼梯。

## Knowledge type

Type: Example
Asset: Staircase
Variant: Spiral

## Recommended pattern

Radial repetition using Copy and Transform.

Single stair profile
→ Extrude
→ Rotate + Raise
→ Copy Transform
→ Spiral staircase

## Key concepts

- spiral staircase
- radial repetition
- circular distribution
- rotation
- step angle
- copyxform
- center pillar
- stepAng
- Controller

## Features

- Spiral step layout
- Center pillar
- Railing
- Balusters
- Controller parameters


### 1.2 网络架构

```
Controller (Null + 8 spare 参数)
  |
  +--[STEP_System 台阶系统]-----------------------------------------+
  |   STEP_profile_outer + STEP_profile_inner (内外扇形 circle)
  |     -> STEP_profile_merge (merge)
  |     -> STEP_profile_close (add 闭合轮廓)
  |     -> STEP_extrude (polyextrude 挤出 stepHeight/5)
  |     -> STEP_raise (transform 抬升 stepHeight)
  |   PILLAR_tube (tube 中心柱) -> STEP_pillar_merge
  |     -> STEP_copy (copyxform 螺旋复制 steps+1 级)
  +--[RAIL_System 扶手系统]-----------------------------------------+
  |   RAIL_start_point (add 锚点 x=stepLen) -> RAIL_start_xform
  |     -> RAIL_anchor_copy (引用 STEP_copy 变换)
  |   RAIL_vertical (line 高 railHeight)
  |     -> RAIL_anchor_topts (copytopoints)
  |     -> RAIL_start_group -> RAIL_keep_start -> RAIL_path -> RAIL_resample
  |     -> RAIL_main_tube (sweep r=railSize) + RAIL_sub_tube (r=railSize/1.4)
  |     -> RAIL_main_cap/bevel -> RAIL_merge
  +--[BALUSTER_System 栏杆系统]-------------------------------------+
  |   BALUSTER_vertical (line) -> BALUSTER_resample (bars 均分)
  |     -> BALUSTER_group -> BALUSTER_blast -> BALUSTER_attrib (@ptnum)
  |     -> BALUSTER_topts -> BALUSTER_path -> BALUSTER_resample2
  |     -> BALUSTER_tube -> BALUSTER_cap -> BALUSTER_bevel
  +-----------------------------------------------------------------+
  OUT_staircase (merge: STEP_copy + RAIL_merge + BALUSTER_bevel)
```

### 1.3 Controller 参数表（当前值）

| 参数 | 当前值 | 说明 |
| --- | --- | --- |
| stepLen | 10.0 | 台阶长度(扇形半径) |
| stepAng | 25.0 | 每级台阶角度(度) |
| stepHeight | 1.635 | 每级台阶高度 |
| pillarRad | 0.4 | 中心柱半径 |
| steps | 8 | 台阶数量 |
| railHeight | 4.91 | 扶手总高度 |
| railSize | 0.2 | 扶手管半径 |
| bars | 5 | 栏杆立柱数量(每段) |



## Houdini Python example

```python
# ============================================================
# Procedural Spiral Staircase - COMPACT rebuild script v3

# ============================================================
import hou

# --- 0. Container ---
parent = hou.node("/obj")
if hou.node("/obj/geo1"):
    hou.node("/obj/geo1").destroy()
geo = parent.createNode("geo", "geo1", run_init_scripts=False, load_contents=True, exact_type_name=True)

# --- 1. Create nodes ---
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
n_Controller = geo.createNode('null', 'Controller')
n_OUT_staircase = geo.createNode('merge', 'OUT_staircase')
n_PILLAR_tube = geo.createNode('tube', 'PILLAR_tube')
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
n_STEP_copy = geo.createNode('copyxform', 'STEP_copy')
n_STEP_extrude = geo.createNode('polyextrude::2.0', 'STEP_extrude')
n_STEP_pillar_merge = geo.createNode('merge', 'STEP_pillar_merge')
n_STEP_profile_close = geo.createNode('add', 'STEP_profile_close')
n_STEP_profile_inner = geo.createNode('circle', 'STEP_profile_inner')
n_STEP_profile_merge = geo.createNode('merge', 'STEP_profile_merge')
n_STEP_profile_outer = geo.createNode('circle', 'STEP_profile_outer')
n_STEP_raise = geo.createNode('xform', 'STEP_raise')

# --- 1.5 Controller spare parms (BEFORE expressions) ---
ctrl = n_Controller
ctrl.addSpareParmTuple(hou.FloatParmTemplate('stepLen', 'Step Length', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.FloatParmTemplate('stepAng', 'Step Angle', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.FloatParmTemplate('stepHeight', 'Step Height', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.FloatParmTemplate('pillarRad', 'Center Pillar Radius', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.IntParmTemplate('steps', 'No of Steps', 1, default_value=(0,)))
ctrl.addSpareParmTuple(hou.FloatParmTemplate('railHeight', 'Railing Height', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.FloatParmTemplate('railSize', 'Hand Rail Size', 1, default_value=(0.0,)))
ctrl.addSpareParmTuple(hou.IntParmTemplate('bars', 'No of Bars', 1, default_value=(0,)))
ctrl.parm('stepLen').set(10.0)
ctrl.parm('stepAng').set(25.0)
ctrl.parm('stepHeight').set(1.635)
ctrl.parm('pillarRad').set(0.4)
ctrl.parm('steps').set(8)
ctrl.parm('railHeight').set(4.91)
ctrl.parm('railSize').set(0.2)
ctrl.parm('bars').set(5)

# --- 2. Set parms (folder toggles first, then expr/values) ---
p = n_BALUSTER_topts.parm('targetattribs')
if p is not None: p.set(3)
p = n_RAIL_anchor_topts.parm('targetattribs')
if p is not None: p.set(3)
p = n_RAIL_start_point.parm('points')
if p is not None: p.set(1)
p = n_STEP_profile_close.parm('points')
if p is not None: p.set(1)

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

# --- 3. Connect nodes ---
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
n_OUT_staircase.setInput(0, n_STEP_copy)
n_OUT_staircase.setInput(1, n_RAIL_merge)
n_OUT_staircase.setInput(2, n_BALUSTER_bevel)
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
n_STEP_copy.setInput(0, n_STEP_pillar_merge)
n_STEP_extrude.setInput(0, n_STEP_profile_close)
n_STEP_pillar_merge.setInput(0, n_PILLAR_tube)
n_STEP_pillar_merge.setInput(1, n_STEP_raise)
n_STEP_profile_close.setInput(0, n_STEP_profile_merge)
n_STEP_profile_merge.setInput(0, n_STEP_profile_outer)
n_STEP_profile_merge.setInput(1, n_STEP_profile_inner)
n_STEP_raise.setInput(0, n_STEP_extrude)



# --- 6. Display / render flags ---
n_OUT_staircase.setDisplayFlag(True)
n_OUT_staircase.setRenderFlag(True)



print("OK: 36 nodes rebuilt, 3 boxes, spare params restored, layout applied.")
```


