# QA Policy

## Purpose

Use this reference after deterministic rendering. The locked artwork must remain source-derived throughout the pipeline.

## PASS conditions

Always require:
- source artwork SHA-256 matches `manifest.json`;
- deterministic warped layer regenerates pixel-identically;
- deterministic final composite regenerates pixel-identically;
- all target quad corners are inside the substrate canvas;
- no non-uniform stretching is used;
- `cover` is used only when explicitly authorized;
- no generative editing is applied after deterministic compositing.

### General
- hue-direction drift caused by presentation lighting: median <= 2 degrees, 95th percentile <= 5 degrees;
- final visual inspection shows no obvious missing logo/text/illustration elements;
- major text remains visually recognizable at intended mockup scale.

### High
- hue-direction drift: median <= 1 degree, 95th percentile <= 3 degrees;
- inspect small text, thin strokes, logo geometry and artwork edges enlarged;
- no unexplained crop, missing detail, or color cast;
- if the target resolution is too low to preserve small details, fail rather than invent them.

## Substrate cleanup checks

For Mode 2A, compare original and cleaned material outside the replacement region.

Suggested thresholds after a small blur to ignore compression noise:
- General: outside-region mean absolute RGB difference <= 6 and changed-pixel fraction <= 10%.
- High: outside-region mean absolute RGB difference <= 3 and changed-pixel fraction <= 5%.

If thresholds fail, retry cleanup with a tighter mask. If repeated attempts fail, require confirmation before Mode 2B.

## What this v1 does not prove

A deterministic QA pass proves that the supplied artwork was not regenerated or silently altered after compositing. It does not prove that a manually chosen target quad perfectly models a strongly curved 3D surface. Treat severe curvature, deep folds, transparency, wraparound graphics and strong specular reflection as geometry-risk cases.

## Material realism check

Material realism is a visual acceptance check, not a license to alter artwork.

For paper goods such as business cards:
- the substrate should read as paper/cardstock rather than plastic or a featureless digital rectangle;
- subtle grain/fiber and realistic edge behavior should be visible when resolution/viewpoint permits;
- material texture must remain subordinate to the printed design;
- if the user specifies a paper stock/finish, match that instead of the default.

## Delivery PASS

QA is not the final gate. Delivery passes only when:
- `mockup.png` exists and can be opened;
- fidelity QA is PASS;
- the mockup image is actually surfaced to the user as a preview/attachment or clickable final file.

A generated-but-unshown image is `delivery failed`, not success.

## Edge preservation check

When the source artwork contains edge-adjacent content, QA must verify that it remains visible and intentional in the final mockup.

Examples:
- a left-side white stripe on a dark business card front must still appear on the front face;
- a thin border around a card must not disappear unless explicitly cropped or physically occluded;
- a keyline near the trim must not be weakened to invisibility by texture or lighting.

Treat this as a PASS/FAIL requirement, not a stylistic preference.

Recommended interpretation:
- If a border/stripe exists in the source and the target face is visible, its corresponding transformed region should also be visible in the final mockup.
- If a very thin line is below reliable display resolution after perspective, prefer a less aggressive viewing angle or a larger face area rather than silently losing it.
