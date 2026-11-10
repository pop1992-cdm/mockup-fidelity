---
name: mockup-fidelity
description: Create and deliver high-fidelity product and surface mockups from PNG/JPG artwork while treating the original artwork as a locked asset. Use when a user asks to place, replace, apply, preview, or mock up a design on business cards, paper goods, packaging, cups, bottles, posters, signs, screens, apparel, bags, or an existing mockup. Preserve artwork content, aspect ratio and base colors, select realistic substrate/material properties, show a preflight configuration, composite deterministically, automatically verify fidelity, and always surface the finished mockup image to the user.
---

# Mockup Fidelity

Create mockups without letting a generative image model redraw the user's artwork.

## Non-negotiable rules

1. Treat every supplied PNG/JPG artwork file as a **locked asset**.
2. Never ask a generative image model to redraw, recreate, reinterpret, repair, restyle, or re-typeset the locked artwork.
3. Separate:
   - **Content layer:** artwork pixels, text, logo, illustration, relative layout, base colors.
   - **Presentation layer:** position, uniform scale, rotation, perspective, surface warp, occlusion, luminance, shadow, highlight, texture.
4. Apply naturalization only to the presentation layer. Never change the content layer to make the mockup look more natural.
5. Preserve the artwork aspect ratio by default. Never stretch non-uniformly.
6. Permit crop/full-bleed/cover only when the user explicitly requests full bleed, wrap, edge-to-edge, crop-to-fill, or equivalent.
7. Always run fidelity verification after rendering. Do not silently deliver a failed mockup.
8. Never silently switch from precise replacement to regenerated-material fallback.
9. Do not make users install desktop software. Use available image tools and bundled scripts.
10. Treat material realism as a separate **substrate/material layer**. Never fake paper, fabric, plastic, metal, or other surface character by repainting the artwork.
11. Do not declare the task complete until the finished mockup image itself is visible or attached in the user-facing response. A console message, file path, QA report, or “done” message alone is not delivery.
12. Success requires all three gates: **Render PASS → Fidelity QA PASS → Delivery PASS**.
13. Treat border lines, side stripes, trim-adjacent color bands, keylines, and any artwork element close to the cut edge as **content-layer elements**. They must remain visible after mockup unless they are physically occluded by the substrate or explicitly cropped with user authorization.
14. Before any image generation or image editing begins, establish whether the output is **proposal-use**. If the user has not already explicitly said yes/no, ask exactly one proposal-use question and wait for the answer. Never generate the image before this decision is known.

## Inputs

Accept:
- Locked artwork: PNG or JPG. Prefer transparent PNG when available.
- Material/mockup image: optional. It may be blank or may already contain artwork.
- Optional placement guidance:
  1. user-provided selection/mask/annotation;
  2. user text description;
  3. automatic detection.
- Optional fidelity mode: `general` or `high`.
- Proposal-use decision: `yes` or `no`. This is required before image generation; infer it only when the user explicitly states the output is for a proposal/presentation or explicitly says it is not.

Do not require connectors. Do not require Photoshop, Illustrator, Blender, or other local software.

## Edge, bleed, and trim preservation

Before compositing, inspect whether the artwork contains any element that sits near or touches the trim edge:
- border lines;
- full-height side stripes;
- top/bottom color bars;
- thin keylines;
- logos or text aligned close to an edge;
- intentional bleed/full-bleed backgrounds.

Treat these as **edge-adjacent content**.

Rules:
1. Do not let automatic framing or perspective placement hide edge-adjacent content by accident.
2. In `contain` mode, preserve the entire artwork including edge-adjacent content.
3. In `cover` mode, crop only when the user explicitly requested full bleed / crop-to-fill / wrap, and report that crop in preflight.
4. When a card or package is shown at an angle, distinguish the **front-face printed stripe** from the **object thickness/side wall**. Do not let a front-face stripe vanish because the model treats it as the side thickness.
5. If the substrate or camera angle causes a very thin edge element to risk disappearing, adjust framing/angle or reduce occlusion so the edge-adjacent content stays visible.
6. If physical occlusion is genuinely unavoidable, call it out in preflight and ask for confirmation in high-fidelity mode.

For business cards specifically, a left or right vertical brand stripe on the printed face must stay visible on the face itself. It is not acceptable for the stripe to disappear and leave only the exposed paper thickness visible.

## Placement priority

Resolve placement in this order:

1. User selection, mask, or annotation.
2. User text description.
3. Automatic detection.

If automatic detection has multiple plausible targets, unclear boundaries, severe occlusion, or strong curvature, treat placement as uncertain and require confirmation before rendering.

## Material-aware substrate workflow

Determine the physical substrate before rendering. Read `references/material-presets.md` when the user names an object/material or when a substrate must be generated.

Use this priority:
1. user explicitly specified material/finish;
2. visible material in the provided mockup;
3. object-specific default preset;
4. neutral realistic default.

For business cards, name cards, invitation cards, postcards, stationery, and similar paper goods, do **not** default to a featureless flat white rectangle. Unless the user specifies otherwise, default to:
- premium uncoated cardstock;
- subtle paper fiber/grain visible mainly in highlights and close edges;
- realistic card thickness at exposed edges;
- soft contact shadow;
- low-to-moderate roughness;
- no printed graphics before deterministic artwork compositing.

If generating a blank substrate with an image model, prompt for the **unprinted material only**. Explicitly request no text, no logo, no illustration, no placeholder graphics, and no watermark. After generation, composite the locked artwork deterministically.

If the provided substrate is unnaturally smooth but the object class requires visible material character, add a deterministic material texture to the substrate before artwork compositing using `scripts/apply_material_texture.py`, when appropriate.

Never use material texture to alter the artwork source pixels. Material interaction belongs to the presentation layer only.

## Rendering modes

Choose one:

- **Mode 1 — blank material:** use the provided blank material, or generate a blank material/substrate when the user did not provide one.
- **Mode 2A — precise replacement:** default when the provided material already contains artwork. Remove the old artwork only from the target region, preserve the rest of the image, then composite the locked artwork deterministically.
- **Mode 2B — regenerated material:** recreate a similar blank material, then composite the locked artwork deterministically. Use only after 2A is unreliable and the user confirms, unless the user explicitly pre-authorized fallback.

Never include the locked artwork in a generative image-editing prompt. Generate or clean the **substrate first**, then composite the original artwork afterward.

## Proposal-use gate — mandatory before image generation

Before generating or editing any image, establish whether the output needs a proposal presentation layout.

If the user has **not** already answered this in the same request or prior conversation context, ask exactly:

`這張 Mockup 是否需要做成提案版？（需要／不需要）`

Rules:
1. Ask this before image generation, image editing, substrate generation, or final mockup rendering.
2. Wait for the answer. Do not begin image generation while the proposal-use decision is unresolved.
3. If the user already explicitly says `提案用`, `簡報用`, `proposal`, or equivalent, treat it as `yes` and do not ask again.
4. If the user explicitly says `不用提案`, `只要 mockup`, or equivalent, treat it as `no` and do not ask again.
5. Record the decision in preflight as `Proposal mode: yes/no`.

### Proposal mode = yes

Read `references/proposal-mode.md`.

Produce a **presentation-ready composite** whose main mockup remains dominant and whose bottom area contains a separate proposal information band inspired by the provided reference layout.

Use three columns:

1. **設計概念**
   - 2–4 short lines explaining the visible design rationale.
   - Ground the copy in the supplied artwork, user brief, and observable brand cues.
   - Do not invent business strategy, brand history, or symbolism that the user did not provide or that is not visually supportable.

2. **品牌元素**
   - Show the original brand mark or exact source-derived visual element.
   - Optionally show a deterministic/extracted motif or color/shape relationship.
   - Do not alter the locked artwork used on the mockup.
   - If a new motif would require invention, use existing shapes/colors instead of fabricating a new logo concept.

3. **材質建議**
   - Name the recommended material/stock/finish.
   - Include a practical specification when appropriate, e.g. `象牙紙（260–300gsm）`.
   - Add one concise tactile/production rationale.
   - Use `references/material-presets.md` for substrate logic.

Layout rules:
- Put the proposal band **below** the main mockup, not on top of the product artwork.
- Keep generous spacing, clear dividers, and presentation-grade typography.
- Keep the main mockup visually larger than the proposal band.
- Do not let the proposal band crop, cover, or visually compete with the locked artwork.
- The bottom band may use neutral background panels, source-derived brand colors, small swatches, and material samples.
- Treat proposal copy as presentation content, not part of the locked artwork.

### Proposal mode = no

Deliver the normal mockup without the proposal information band.

## Preflight: always report settings before execution

Before modifying or generating any image, show a compact configuration summary. Use this structure:

**Mockup preflight**
- Artwork: `[filename]` — Locked
- Material source: `[provided blank / provided existing mockup / AI-generated blank]`
- Material profile: `[paper/cardstock / coated paper / plastic / metal / glass / fabric / screen / other]`
- Material finish: `[matte / uncoated / coated / glossy / satin / textured / user-specified]`
- Mode: `[1 / 2A / 2B]`
- Placement source: `[selection / description / auto-detected + confidence]`
- Fit: `[contain / cover]`
- Edge-adjacent content: `[none detected / detected: preserve full visibility / detected but physically occluded]`
- Proposal mode: `[yes / no]`
- Naturalization: presentation layer only
- Artwork redraw: prohibited
- Fidelity: `[general / high]`
- Verification: text/content, composition, aspect ratio, base color, detail integrity
- Retry budget: `[2 / 4]`
- 2A → 2B fallback: `[not authorized / authorized]`

For `general`, append: `可說「高保真」切換為更嚴格驗證。`

### Conditional confirmation

Continue automatically after preflight when all material decisions are explicit and low-risk.

Stop and ask for confirmation only when at least one of these applies:
- placement is inferred with low or ambiguous confidence;
- full-bleed/cropping would be inferred rather than explicitly requested;
- 2A needs to fall back to 2B without prior authorization;
- strong curvature, heavy folds, transparency, reflection, or occlusion makes faithful placement uncertain;
- a requested action would violate a locked-artwork rule.

If the user explicitly chose a high-risk option already, do not ask them to confirm the same choice again.

## Fidelity modes

Default to `general` when unspecified.

Interpret these as `high`: high fidelity, 高保真, 嚴格驗證, 品牌色不能跑, 小字不能變, pixel-perfect.

Interpret these as `general`: 一般, 快速, 概念稿, preview.

### General
- Run all deterministic integrity checks.
- Retry failed rendering up to 2 times.
- Allow realistic luminance/shadow/highlight changes on the presentation layer.
- Require obvious text/logo/illustration structure to remain intact.

### High
- Run all deterministic integrity checks plus stricter visual inspection.
- Retry failed rendering up to 4 times.
- Reduce presentation-layer lighting strength when it compromises color appearance.
- Inspect small text, thin lines, logo geometry, crop boundaries, and color appearance at enlarged scale.

## Core workflow

1. Inspect inputs and determine whether proposal-use is already explicit.
2. If proposal-use is unresolved, ask the mandatory proposal-use question and wait for the answer.
3. Determine rendering mode.
4. Determine placement using the priority rules.
5. Inspect the artwork for edge-adjacent content and set an edge-preservation strategy.
6. If proposal mode is `yes`, read `references/proposal-mode.md` and prepare grounded proposal copy/visual elements before rendering.
7. Emit the preflight summary, including `Proposal mode`.
8. Apply conditional-confirmation rules.
9. Prepare a blank/clean substrate.
   - For Mode 2A, use image editing only to remove the existing design from the target area.
   - If an edit changes unrelated areas materially, reject it and retry.
10. Composite the locked artwork using deterministic processing.
   - Prefer `scripts/render_mockup.py`.
   - Use `contain` by default.
   - Use `cover` only with explicit user authorization.
   - Use only presentation-layer luminance modulation for material integration.
11. Run `scripts/verify_mockup.py`.
12. Perform final visual inspection of the rendered mockup.
13. If verification fails, retry within the fidelity-mode budget.
14. If proposal mode is `yes`, compose the bottom proposal information band **after** the core mockup passes fidelity QA. Do not modify the locked artwork layer while adding the presentation band.
15. Verify proposal layout:
   - all three sections are present;
   - copy is grounded in source/user information;
   - brand visuals are source-derived;
   - material recommendation is plausible;
   - band does not cover or crop the mockup.
16. If verification still fails, stop and report:
    - failed check;
    - probable cause;
    - recommended fix or fallback.
17. Run the **Delivery Gate** below.
18. Deliver only a passing result, or clearly label a non-passing result as failed instead of presenting it as successful.

## Delivery Gate — mandatory

A mockup is not complete merely because a file was generated.

Before saying the task is finished:
1. Confirm the final render file exists and is readable.
2. Confirm fidelity verification is PASS.
3. Surface the final mockup image in the same user-facing turn:
   - Prefer an actual image attachment/preview produced by the available image/file tool.
   - If the environment returns only a file, provide a direct clickable file link and clearly identify it as the final mockup.
   - If the platform supports both preview and link, provide both.
4. Never respond only with “completed”, a tool log, a filesystem path, or QA text.
5. If the image cannot be surfaced, report `Status: delivery failed`, then retry delivery. Do not claim the mockup was delivered.

For normal successful delivery, keep the accompanying text brief:
- show the image first when the interface permits;
- then state fidelity mode and QA PASS;
- mention any material preset used.

## Deterministic compositor

Use:

```bash
python scripts/render_mockup.py \
  --base clean_material.png \
  --artwork design.png \
  --quad "x1,y1 x2,y2 x3,y3 x4,y4" \
  --fit contain \
  --fidelity general \
  --out-dir output
```

Order the quad points: top-left, top-right, bottom-right, bottom-left.

The compositor writes:
- `mockup.png`
- `warped_artwork.png`
- `presentation_artwork.png`
- `mask.png`
- `manifest.json`

Do not run a generative image model on `mockup.png` after deterministic compositing. Any later generative edit invalidates the locked-artwork guarantee and must be discarded or re-composited afterward.

For a plain paper/card substrate that needs physical material character, optionally prepare the base first:

```bash
python scripts/apply_material_texture.py \
  --input blank_card.png \
  --material uncoated-cardstock \
  --strength 0.32 \
  --output textured_card.png
```

Apply this to the substrate **before** placing artwork.

## Verification

Run:

```bash
python scripts/verify_mockup.py \
  --out-dir output \
  --artwork design.png
```

Verification must check:
- artwork file hash matches the render manifest;
- presence/integrity of edge-adjacent content such as stripes, borders, and trim-side keylines;
- warped content can be regenerated exactly from the source;
- final composite can be regenerated exactly from the source + base;
- target region stays inside the canvas;
- the base color layer has not been generatively changed;
- presentation-layer naturalization does not introduce meaningful hue rotation.

Use `references/qa-policy.md` for PASS/FAIL interpretation and limitations.

## Existing mockup protection

When Mode 2A requires generative cleanup, compare the original material with the cleaned substrate outside the target region. If the environment supports deterministic image comparison, use `scripts/verify_substrate.py`.

If cleanup repeatedly modifies unrelated areas, do not hide this. Offer:
- a tighter user selection/mask;
- Mode 2B with confirmation;
- a simpler/blank material image.

## Curves, folds, and 3D limits

This v1 is optimized for flat and near-flat 2D/2.5D surfaces with perspective and moderate lighting variation.

For strong cylinders, deep folds, transparent materials, complex reflections, or wraparound artwork:
- preserve the locked-artwork rule;
- do not fake fidelity by generatively redrawing the artwork;
- mark the case as high-risk in preflight;
- use the best available geometry/warp tool if present;
- otherwise explain that v1 cannot guarantee accurate surface mapping and request confirmation before a less exact fallback.

## Regression discipline

Treat every discovered mockup defect as a reusable regression case, not only as a one-off prompt correction.

Read:
- `references/failure-taxonomy.md` when a render, QA step, fallback, or delivery fails.
- `references/regression-tests.md` after changing rendering, material, QA, fallback, edge-preservation, proposal-mode, or delivery behavior.
- `references/proposal-mode.md` whenever proposal mode is enabled or its presentation rules change.

Rules:
1. Assign at least one failure code to every meaningful failure.
2. Fix the root workflow rule before adding prompt-only wording.
3. Add or update a regression case when the failure represents a reusable class.
4. Before packaging an updated skill, run all impacted regression cases and all P0 release-gate cases that can be executed in the current environment.
5. Never mark `BLOCKED` as `PASS`.
6. Block release on any new P0 FAIL or any new S0/S1 regression.
7. If some image-generation regression cases cannot be executed in the current environment, explicitly report them as `BLOCKED/NOT_RUN`; still run deterministic and structural checks.

Use the bundled helper:

```bash
python scripts/regression_report.py init --output regression-report.json
python scripts/regression_report.py check --report regression-report.json
```

The helper enforces the P0 release gate for recorded case results.

## Failure policy

Use `references/failure-taxonomy.md` to classify every meaningful failure. Never loop indefinitely.

After retries are exhausted, report:
- `Status: fidelity check failed`
- failed categories: content / placement / crop / edge-preservation / color / substrate / presentation
- cause
- next best action

Do not call a result “high fidelity” when any required check is unresolved.
Use `references/edge-preservation.md` whenever the artwork has border lines, side stripes, keylines, trim-edge logos, or other elements close to the cut edge.

## Test the skill

Use `references/test-cases.md` after installation to pressure-test preflight, fallback, fidelity, placement, and failure behavior.
