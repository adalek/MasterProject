Generate only executable Houdini Python code.
Do not use Markdown code fences.
Do not explain the solution.

Create a procedural straight staircase inside one Geometry container under /obj.

Create a Null SOP named STAIR_CONTROLS.

Add these editable parameters to STAIR_CONTROLS:
- num_steps: integer, default 12, minimum 2
- total_height: float, default 3.0
- step_depth: float, default 0.3
- step_width: float, default 1.2

Create:
- one Box SOP for a single step
- one Attribute Wrangle SOP to generate step points
- one Copy to Points SOP
- one Merge SOP

Requirements:
- The staircase must update when parameters on STAIR_CONTROLS change.
- Do not hard-code num_steps, total_height, step_depth or step_width into VEX.
- Use ch() expressions in VEX to reference STAIR_CONTROLS.
- Copy to Points input 0 must be the Box SOP.
- Copy to Points input 1 must be the Attribute Wrangle SOP.
- Set the Merge SOP as display and render node.
- Execute immediately inside Houdini.