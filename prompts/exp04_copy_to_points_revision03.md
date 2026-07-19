Generate only executable Houdini Python code.
Do not use markdown code fences.
Do not explain your solution.

Create these SOP nodes inside one geometry container:
Create:
- one geometry container under /obj
- one Box SOP
- one Grid SOP
- one Scatter SOP
- one Copy to Points SOP

You must connect them using exactly these statements:

scatter.setInput(0, grid)
copytopoints.setInput(0, box)
copytopoints.setInput(1, scatter)

Then set:
copytopoints.setDisplayFlag(True)
copytopoints.setRenderFlag(True)



Layout the nodes.

Output executable Python only.