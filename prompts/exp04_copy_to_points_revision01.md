Generate only executable Houdini Python code.

Do not use markdown code fences.
Do not explain your solution.

Create:
- one geometry container under /obj

Create the following SOP network:

Grid
↓

Scatter
↓

Copy to Points

The first input of Copy to Points must be the geometry to copy.

The second input must be the template points.

Set Copy to Points as the display node.

Copy one Box SOP onto the scattered points.

Layout the nodes.

Output executable Python only.