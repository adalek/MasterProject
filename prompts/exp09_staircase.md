Generate only executable Houdini Python code.
Do not use Markdown code fences.
Do not explain the solution.

Create a simplified procedural spiral staircase inside one Geometry container under /obj.

Create:
- one Box SOP for a single stair tread
- one Attribute Wrangle SOP to generate points
- one Copy to Points SOP
- one Merge SOP

Use these values:
- num_steps = 32
- radius = 2.0
- total_height = 4.0
- angle_step = 11.25 degrees
- tread_depth = 0.45
- tread_width = 1.2
- tread_height = total_height / num_steps

For point index i:
- angle = radians(i * angle_step)
- x = cos(angle) * radius
- z = sin(angle) * radius
- y = i * tread_height

VEX requirements:
- Use radians(), sin(), and cos().
- quaternion() must return vector4.
- Use quaternion(rotation_angle, {0, 1, 0}).
- Store the result as the point attribute orient.
- Do not pass four scalar values to quaternion().
- Each stair must face radially outward.
- Apply a 90-degree rotation offset if needed.
- Adjacent steps should slightly overlap.
- Do not use undefined constants such as pi.

Copy to Points input 0 must receive the Box SOP.
Copy to Points input 1 must receive the Attribute Wrangle SOP.
Set the Merge SOP as display and render node.
Execute immediately inside Houdini.