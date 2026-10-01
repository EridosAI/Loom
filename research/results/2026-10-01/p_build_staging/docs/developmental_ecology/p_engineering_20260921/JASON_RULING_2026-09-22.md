# Jason's ruling — user-message transcription

Source: Jason's instruction in this local task, received 2026-09-22. This is a new branch implementation record, not an edit to the historical specification.

Resolve OPEN_ISSUE_LIGHT_BOUNDARY.md as follows.

The fixed distant directional illumination crosses the arena boundary.
The arena is modelled as an open optical domain under an external
distant directional source, not as a sealed opaque 2D box.

For directional-shadow evaluation:

- Reaching the arena boundary without first intersecting a finite
  in-arena opaque body means the point receives the directional
  illumination. The boundary wall does not block entry of the
  external directional field.
- Finite solid bodies inside the arena may occlude the directional
  component and cast geometric shadows according to the implemented
  light direction and geometry.
- The weak ambient illumination component remains present in shadow
  and is not blocked by this directional-shadow test.
- Arena walls remain perceptible physical/material structures and
  participate normally in visual surface response and contact. Do
  not implement their illumination behaviour by assigning them a
  special transparent material. The distinction is the optical-domain
  boundary condition.
- Wall-mounted restorative surfaces follow the boundary treatment
  unless their represented geometry protrudes into the arena, in
  which case the protruding interior geometry may cast an ordinary
  finite-body shadow.

Record this as the selected implementation realization of the already
accepted fixed directional + ambient illumination law. Preserve the
alternative closed-wall interpretation in the issue record as rejected
for this branch because it suppresses the directional component across
the interior and defeats the intended global-asymmetry/shading function.

This ruling does not authorize any other physical-law change, parameter
tuning, scientific run, or mechanism alteration.

Continue the previously authorized bounded engineering build and
verification from commit
bf5df05ad2aafb8590e8765a947df111956b9528.

Do not restart or redesign completed work. Finish the blocked baseline
fixture, complete the named engineering checks and complete-loop smokes
within the existing authorization, update the build report and portable
review package, and stop at the originally specified review boundary.
