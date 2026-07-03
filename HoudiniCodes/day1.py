# day1.py

import hou

# Create a new geometry node
box_node = hou.node('/obj').createNode('geo', 'my_box')

# Create a new box primitive
box_prim = box_node.createNode('box', 'my_box_prim')

# Set the size of the box
box_prim.parm('sizex').set(2.0)
box_prim.parm('sizey').set(2.0)
box_prim.parm('sizez').set(2.0)

# Set the position of the box
box_prim.parm('tx').set(0.0)
box_prim.parm('ty').set(0.0)
box_prim.parm('tz').set(0.0)

print("Box created successfully!")

'''

'''