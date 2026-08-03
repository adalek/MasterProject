Create a simplified spiral staircase using rectangular Box steps.

Create 20 points around a circle.
For point index i:
- angle = radians(i * 18)
- y = i * 0.2
- x = cos(angle) * radius
- z = sin(angle) * radius

Create an orient quaternion so each step faces tangentially around the circle.
Use Copy to Points.
Use radians(), sin(), cos() and quaternion().
Do not use pi or PI constants.
A small overlap between neighboring steps is acceptable.

VEX quaternion rules:

- quaternion() returns vector4, not vector.
- Use quaternion(angle_in_radians, rotation_axis).
- For Y-axis rotation:
  vector4 orient = quaternion(angle, {0, 1, 0});
- Store orientation as a point attribute named orient.
- Do not pass four scalar values to quaternion().