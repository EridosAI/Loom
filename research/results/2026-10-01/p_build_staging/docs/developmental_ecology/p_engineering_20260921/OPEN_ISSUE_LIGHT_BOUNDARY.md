# Directional illumination boundary — resolved for this branch

**Selected by Jason, 2026-09-22:** the arena is an open optical domain under the already accepted external distant directional source. This is an implementation realization of fixed directional plus ambient light; no other physical law or mechanism is changed.

A shadow ray that reaches the arena boundary before an in-arena finite opaque body receives the directional component. Finite interior geometry, including the organism, can block that component. The weak ambient component remains in shadow. Walls still have M1 reflectance, terminate ordinary visual rays and participate in contact. No wall has been assigned a transparent material.

Wall-mounted restorative surfaces follow the domain boundary unless their geometry protrudes inside it. The specified 0.25-diameter-thick restorative rectangles do protrude, so their interior geometry casts ordinary finite-body shadows. A zero-thickness flush boundary surface does not prevent the external field entering.

Configuration: `illumination_boundary="open"`. `geometry.directional_visible` caps the shadow ray at its first exit from the square; only finite intersections strictly before that exit block the directional component. Surface shading, spectrum, ambient fraction, attenuation, sensor rays and material palette remain source-derived and unchanged.

The closed-wall interpretation is **rejected for this branch**: it suppresses the directional component throughout the interior and defeats the intended global-asymmetry/shading function. It remains recorded below and available as an explicitly named arithmetic comparison (`opaque`), never a substituted baseline. This ruling authorizes no tuning, scientific run or other mechanism alteration.

Verification: `test_open_domain_finite_shadow_boundary_and_protruding_repair` checks boundary entry, finite occluders, flush/protruding restorative geometry and unchanged wall material/visual intersection. `test_ambient_survives_shadow_and_directional_surface_response` checks positive ambient in shadow and the restored directional response. The original preparation's geometry/chemistry/random-stream dependencies are verified before cached fields are reused.

## Preserved original issue at checkpoint bf5df05ad2aafb8590e8765a947df111956b9528

The following text records the earlier unresolved state; its pending statements are superseded by Jason's ruling above.

# Required ruling: directional illumination at the arena boundary

Status: unresolved; asked Jason during this build. No answer has been assumed. This is not a request to revisit D1–D3.

Sources: P_IMPLEMENTATION_AND_OBSERVATION_SPEC_v0_1_REVIEW_DRAFT.md §8.3 defines a fixed distant light, a visibility factor toward that light, and first solid hits in a closed square whose walls share M1 with the mover (§8.1). PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md §§3.2, 6.1–6.2 requires perceptible physical boundaries and directional plus ambient illumination. No wall height, over-wall light rule, or optical boundary exception is specified.

Two readings:

1. Walls occlude directional illumination like the other M1 solids. Every outward planar light ray from an interior point eventually meets a wall, so the directional term is suppressed throughout the enclosed arena. The ambient term remains.
2. The fixed distant illumination enters across the arena boundary; walls still terminate visual rays, and interior solids including the organism occlude illumination. This supplies the intended directional shading but requires an explicit boundary exception not stated in the source.

Smallest resolution: choose one illumination-boundary convention explicitly and record it in the engineering annex/configuration. No packet, cortical, associative, regulatory or body-accounting law need change. Neither reading has been chosen as the baseline. Config.illumination_boundary remains null and light_readings raises on an unresolved boundary. Opaque-light settings used in transducer and snapshot component fixtures are fixture assumptions only, not a selected baseline.

Question asked: should walls also block illumination rays, or should directional light illuminate the arena across its boundary?

Independent work continued: neural and physical component implementation/tests, exact world-only field prehistory, snapshot/record components, fixed information-loss diagnostics and paused inspector shell. The three declared complete-loop cases remain unexecuted. No baseline is represented as verified.
