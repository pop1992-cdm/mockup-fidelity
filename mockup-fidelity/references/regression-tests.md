# Mockup Regression Test Suite

Run this suite after changing SKILL.md, rendering rules, material presets, QA rules, or image-processing scripts.

## Release gate

A new skill package is ready only when:
- all **P0** cases PASS;
- no new S0/S1 failure appears versus the previous version;
- any intentionally accepted S2/S3 issue is documented;
- the packaged skill still validates.

Do not waive P0 failures for visual polish reasons.

## Required report fields

For every case record:
- Case ID
- Priority
- Input type
- Fidelity mode
- Rendering mode
- Expected invariant(s)
- Result: PASS / FAIL / BLOCKED
- Failure code(s), if any
- Notes
- Artifact path/link, when available

## Fixed regression cases

### R01 — Edge stripe preservation
Priority: **P0**

Input:
- business-card artwork with a full-height stripe touching the left trim edge.

Prompt:
「請 mockup 此名片。」

Expected:
- edge-adjacent content detected in preflight;
- `contain` by default;
- stripe remains visible on the printed front face;
- exposed paper thickness does not replace the stripe.

Fail examples:
- `CNT-04 edge-element-loss`
- `OCC-02 critical-edge-occluded`

### R02 — Thin border preservation
Priority: **P0**

Input:
- card/poster with a thin border close to all four trim edges.

Expected:
- all visible face edges retain the border;
- no unauthorized crop;
- texture/lighting does not erase the keyline.

Fail examples:
- `CNT-04`
- `GEO-05`

### R03 — Aspect ratio / no stretch
Priority: **P0**

Input:
- artwork whose aspect ratio differs substantially from target area.

Expected:
- defaults to `contain`;
- no non-uniform stretching;
- empty margin is preferable to deformation.

Fail examples:
- `GEO-01`
- `GEO-05`

### R04 — Small text and logo integrity
Priority: **P0**

Input:
- business card or packaging with small text, fine icons, and logo.

Prompt:
「高保真，小字與 logo 不可變形。」

Expected:
- high fidelity mode;
- text/logo are source-derived;
- small details remain readable at practical viewing scale;
- no invented glyphs.

Fail examples:
- `CNT-02`
- `CNT-03`
- `FLW-06`

### R05 — Brand color preservation
Priority: **P0**

Input:
- artwork with at least one strong brand color and neutral substrate.

Expected:
- base artwork color remains source-derived;
- material lighting may alter luminance but not materially rotate hue;
- high mode uses stricter tolerance.

Fail examples:
- `CLR-01`
- `CLR-03`

### R06 — Existing mockup precise replacement
Priority: **P0**

Input:
- existing mockup with old artwork on a clearly bounded surface.

Expected:
- Mode 2A first;
- old design removed only from target area;
- unrelated material/background preserved;
- new locked artwork composited deterministically.

Fail examples:
- `MAT-06`
- `FLW-01`
- `CNT-02`

### R07 — 2A fallback authorization
Priority: **P0**

Input:
- existing mockup where precise cleanup repeatedly damages surrounding material.

Expected:
- do not silently switch to Mode 2B;
- ask user unless fallback was pre-authorized.

Fail examples:
- `FLW-01`
- `FLW-03`

### R08 — Business card material realism
Priority: **P1**

Input:
- business-card artwork only; no substrate image.

Expected:
- default premium uncoated cardstock;
- subtle paper character;
- plausible exposed edge thickness and soft contact shadow;
- artwork remains locked.

Fail examples:
- `MAT-01`
- `MAT-02`
- `MAT-04`

### R09 — Material texture must not obscure print
Priority: **P1**

Input:
- thin type and fine rules on textured paper.

Expected:
- texture remains subordinate;
- printed details remain readable.

Fail examples:
- `MAT-03`
- `CNT-03`

### R10 — User-selected placement wins
Priority: **P0**

Input:
- target image with user annotation/selection and conflicting plausible auto placement.

Expected:
- user selection outranks description and auto detection.

Fail examples:
- `GEO-02`

### R11 — User-described placement wins over auto
Priority: **P1**

Prompt:
「放在杯身正中央、把手左側，不要滿版。」

Expected:
- placement source = description;
- auto detection does not override it.

Fail examples:
- `GEO-02`

### R12 — Explicit full bleed
Priority: **P0**

Prompt:
「做滿版 full bleed，可以裁切，但 logo 不能拉伸。」

Expected:
- cover/crop allowed;
- crop is explicit in preflight;
- no non-uniform stretch.

Fail examples:
- `GEO-01`
- `GEO-05`

### R13 — Strong curvature risk
Priority: **P1**

Input:
- strongly curved bottle or wraparound surface with text/logo.

Expected:
- geometry risk flagged;
- no false high-fidelity claim;
- confirmation required if exact mapping cannot be guaranteed.

Fail examples:
- `GEO-04`
- `FLW-03`

### R14 — Avoidable occlusion
Priority: **P1**

Input:
- two-card composition where one card can cover another.

Expected:
- important text, border, side stripe, or logo is not needlessly hidden;
- if overlap conflicts with critical artwork, alter composition.

Fail examples:
- `OCC-01`
- `OCC-02`

### R15 — Delivery gate
Priority: **P0**

Scenario:
- `mockup.png` exists and QA passes, but final image is not yet surfaced.

Expected:
- task remains incomplete;
- assistant attaches/previews or links the actual final image;
- must not say only "done" or "QA PASS".

Fail examples:
- `DLV-01`
- `DLV-04`

### R16 — Failed QA must not be delivered as success
Priority: **P0**

Scenario:
- deterministic or visual QA is FAIL.

Expected:
- result is labeled failed;
- retry within budget;
- if exhausted, report failure rather than presenting as finished.

Fail examples:
- `DLV-03`
- `FLW-04`

## Run cadence

Run the full suite:
- after changing locked-artwork rules;
- after changing fit/crop/perspective behavior;
- after changing material/naturalization rules;
- after changing fallback or confirmation logic;
- after changing QA/delivery rules.

For a narrow change, run the impacted P0/P1 cases first, then run all P0 cases before packaging.

## Regression decision rule

- **PASS:** expected invariants hold.
- **FAIL:** at least one invariant is violated.
- **BLOCKED:** required capability/input is unavailable; do not reinterpret BLOCKED as PASS.

A previous failure becoming PASS is a fix.
A previous PASS becoming FAIL is a regression and blocks release if P0 or severity S0/S1.
