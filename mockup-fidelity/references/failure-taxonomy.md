# Failure Taxonomy

Use these codes whenever a mockup fails, retries, regresses, or needs user confirmation.
Do not report only "looks wrong." Assign at least one failure code.

## Severity

- **S0 — Blocker:** violates locked-artwork guarantees, delivers no image, or silently changes mode.
- **S1 — Major:** materially changes design, placement, substrate, crop, or brand appearance.
- **S2 — Moderate:** visible realism/quality issue that does not alter artwork content.
- **S3 — Minor:** polish issue; acceptable for draft/general mode but worth improving.

## Failure codes

### CONTENT
- `CNT-01 missing-element` — source text/logo/shape/line disappears.
- `CNT-02 altered-element` — source element is redrawn, misspelled, reshaped, or substituted.
- `CNT-03 detail-loss` — thin stroke, small text, icon, or fine detail becomes unreadable.
- `CNT-04 edge-element-loss` — border, side stripe, keyline, or trim-adjacent element disappears.
- `CNT-05 unauthorized-content` — new text/logo/graphics appear that were not in the source.

Default severity: S0 for CNT-02/CNT-05; S1 for CNT-01/CNT-04; S1–S2 for CNT-03.

### GEOMETRY
- `GEO-01 nonuniform-stretch` — artwork aspect ratio is distorted.
- `GEO-02 placement-wrong` — artwork is on the wrong face/area or substantially misaligned.
- `GEO-03 perspective-wrong` — artwork does not follow the intended plane/perspective.
- `GEO-04 curvature-wrong` — artwork warp does not follow the physical surface.
- `GEO-05 crop-unauthorized` — artwork is cropped without explicit authorization.
- `GEO-06 scale-wrong` — artwork is materially too large/small for the intended placement.

Default severity: S0 for GEO-01/GEO-05; S1 for the rest.

### COLOR
- `CLR-01 hue-shift` — visible hue rotation/color cast beyond mode tolerance.
- `CLR-02 contrast-loss` — lighting/material interaction makes artwork lose intended contrast.
- `CLR-03 brand-color-loss` — a brand-critical color is no longer acceptably represented.
- `CLR-04 substrate-color-wrong` — material/base color does not match user request.

Default severity: S1 for CLR-03; S1–S2 for others.

### SUBSTRATE / MATERIAL
- `MAT-01 wrong-material` — object reads as the wrong material.
- `MAT-02 material-too-flat` — substrate looks like a featureless digital rectangle.
- `MAT-03 texture-too-strong` — texture competes with or obscures artwork.
- `MAT-04 thickness-wrong` — exposed card/paper/object thickness is implausible.
- `MAT-05 reflection-wrong` — highlight/reflection behavior contradicts material.
- `MAT-06 cleanup-damage` — removing old artwork changes unrelated substrate/background.

Default severity: S1 for MAT-06; S2 for MAT-01/04/05; S2–S3 for MAT-02/03.

### OCCLUSION / COMPOSITION
- `OCC-01 avoidable-occlusion` — another object/shadow hides important artwork unnecessarily.
- `OCC-02 critical-edge-occluded` — overlap/shadow hides a border/side stripe/keyline.
- `OCC-03 framing-cuts-object` — composition crops the physical mockup unintentionally.
- `OCC-04 face-not-readable` — viewpoint is so extreme that the intended design face is not useful.

Default severity: S1 for OCC-02; S2 for others.

### MODE / WORKFLOW
- `FLW-01 silent-fallback` — Mode 2A silently changes to 2B without authorization.
- `FLW-02 preflight-missing` — required preflight was skipped.
- `FLW-03 confirmation-missing` — a high-risk choice proceeded without required confirmation.
- `FLW-04 qa-skipped` — fidelity verification was not performed.
- `FLW-05 retry-limit-exceeded` — retry budget was exceeded or looped indefinitely.
- `FLW-06 source-not-locked` — workflow allowed generative editing of locked artwork.

Default severity: S0 for FLW-01/04/06; S1 for FLW-02/03/05.

### PROPOSAL
- `PRP-01 proposal-question-skipped` — image generation/editing started before proposal-use was explicitly resolved.
- `PRP-02 proposal-panel-missing` — user chose proposal mode but the final presentation board lacks the required bottom information band.
- `PRP-03 unsupported-proposal-copy` — proposal copy invents unsupported strategy, history, symbolism, or claims.
- `PRP-04 brand-element-invented` — proposal panel redraws/replaces the source brand mark or invents a new brand element without authorization.
- `PRP-05 proposal-layout-obscures-mockup` — proposal band covers/crops/competes with the mockup instead of sitting beneath it.
- `PRP-06 material-recommendation-missing` — proposal mode lacks a practical material/stock/finish recommendation.
- `PRP-07 stale-output-mode` — a new mockup job reuses the proposal/pure-mockup choice from a previous job instead of resetting to `UNRESOLVED`.

Default severity: S0 for PRP-01/07; S1 for PRP-02/03/04/05/06.

### DELIVERY
- `DLV-01 image-not-surfaced` — render exists but user cannot see/access final image.
- `DLV-02 wrong-file-delivered` — intermediate or failed render delivered as final.
- `DLV-03 qa-failed-but-delivered` — failed result presented as successful.
- `DLV-04 broken-link` — final asset link/attachment is unusable.

Default severity: S0.

## Failure report format

Use this compact structure:

- Status: `FAIL`
- Case: `[regression case id or user task]`
- Code: `[e.g. CNT-04]`
- Severity: `[S0/S1/S2/S3]`
- Evidence: `[what visibly or deterministically failed]`
- Cause hypothesis: `[most likely reason]`
- Retry action: `[what changes on next attempt]`
- Escalation: `[ask user / switch mode with approval / stop]`

If multiple failures occur, list the highest-severity code first.

## Retry mapping

- `CNT-*` → re-composite from locked source; reduce occlusion/texture; never regenerate source content.
- `GEO-*` → recompute placement/quad/fit/warp; preserve aspect ratio.
- `CLR-*` → reduce presentation lighting/color interaction; re-check source color.
- `MAT-*` → change substrate/material treatment only.
- `OCC-*` → change scene composition/viewpoint/overlap.
- `FLW-*` → stop; correct workflow before rendering again.
- `PRP-*` → stop proposal composition; resolve proposal decision/content/layout without altering the already-passing mockup.
- `DLV-*` → retry delivery; do not re-render unless image itself failed.
