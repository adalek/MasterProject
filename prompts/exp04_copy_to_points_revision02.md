Generate only executable Houdini Python code.
Do not use markdown code fences.
Do not explain your solution.

Create:
- one geometry container under /obj
- one Box SOP
- one Grid SOP
- one Scatter SOP
- one Copy to Points SOP

Connections:
- Grid connects to Scatter input 0.
- Box connects to Copy to Points input 0.
- Scatter connects to Copy to Points input 1.

Set Copy to Points as the display and render node.
Layout the nodes.

Output executable Python only.