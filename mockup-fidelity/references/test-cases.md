# Test Cases for Mockup Fidelity v1

Use these prompts to pressure-test the skill after installation.

## 1. Blank flat substrate
Files: transparent PNG artwork + blank poster/card photo.

Prompt:
「把這張設計 mockup 到卡片正面中央。不要裁切。」

Expected:
- Mode 1
- general fidelity unless changed
- auto placement may proceed if unambiguous
- locked artwork
- contain fit
- automatic QA

## 2. Existing artwork replacement
Files: PNG artwork + package photo that already has another label.

Prompt:
「用我的設計精準替換盒子正面的舊標籤，其他地方不要動。」

Expected:
- Mode 2A
- precise cleanup of only the label region
- deterministic re-composite
- substrate comparison outside target area
- no silent Mode 2B fallback

## 3. User-described placement
Prompt:
「放在杯身正中央、把手左側，不要滿版。」

Expected:
- placement source = description
- contain fit
- no non-uniform stretch

## 4. User-selected/annotated placement
Upload an image with a clearly marked target area.

Prompt:
「貼到我圈起來的地方。」

Expected:
- selection/annotation outranks text inference and auto detection

## 5. High fidelity
Use artwork containing small text and a brand color.

Prompt:
「高保真 mockup，小字不能變、品牌色不能跑。」

Expected:
- fidelity = high
- retry budget = 4
- stricter enlarged visual inspection
- no generative redraw of small text

## 6. Ambiguous or strongly curved surface
Use a wrinkled shirt, wraparound bottle, transparent glass, or reflective metal.

Prompt:
「把這個設計貼上去。」

Expected:
- preflight identifies geometry risk
- skill pauses for confirmation if placement/geometry is uncertain
- skill does not claim high fidelity by redrawing the artwork

## 7. Unauthorized fallback
Use an existing complex mockup where clean removal is difficult.

Prompt:
「幫我替換上去。」

Expected:
- start at Mode 2A
- if 2A cannot be preserved, stop and ask before Mode 2B
- must not silently regenerate the whole material

## 8. Explicit full bleed
Prompt:
「做滿版 full bleed，可以裁切，但 logo 不能拉伸。」

Expected:
- fit = cover
- cropping allowed
- non-uniform stretching still prohibited

## 9. Business card material realism
Files: business-card artwork only, no mockup photo.

Prompt:
「幫我做一張名片 mockup。」

Expected:
- material profile defaults to premium uncoated cardstock;
- blank card substrate has subtle paper character, realistic edge thickness and contact shadow;
- artwork is composited afterward as a locked asset;
- final user-facing response visibly includes the resulting mockup image.

## 10. Delivery failure guard
Simulate a run where `mockup.png` exists but the assistant has not surfaced it.

Expected:
- must not say only “完成” or “QA PASS”;
- delivery gate remains incomplete;
- assistant surfaces/attaches the image or a direct final file link before claiming completion.

## 11. Edge-preservation regression: front-face side stripe
Files: an English business-card front whose artwork includes a full-height white stripe along the far-left edge, plus the back side or second face if desired.

Prompt:
「請 mockup 此名片。」

Expected:
- preflight flags edge-adjacent content as detected;
- fit defaults to contain;
- the left white stripe remains visible on the front face of the English card;
- the stripe is not replaced by only the exposed paper thickness;
- if the chosen composition/angle hides the stripe, the render must fail edge-preservation QA and retry or report failure.

## 12. Mandatory proposal-use question
Files: any valid artwork and a mockup request.

Prompt:
「請幫我做這張名片 mockup。」

Expected:
- before any image generation/editing, ask exactly:
  `這張 Mockup 是否需要做成提案版？（需要／不需要）`
- do not generate until the user answers;
- preflight records `Proposal mode: yes/no`.

## 13. Proposal board output
Files: business-card artwork or packaging artwork.

Prompt flow:
1. 「請幫我做這張名片 mockup。」
2. User answers: 「需要提案版。」

Expected:
- normal fidelity workflow runs first;
- passing mockup remains the dominant upper/main image;
- a separate bottom proposal band is added afterward;
- the band has exactly three sections:
  - 設計概念
  - 品牌元素
  - 材質建議
- design concept is grounded in user brief/visible cues;
- brand visuals are source-derived and do not redraw the locked logo;
- material recommendation includes practical stock/finish guidance;
- panel does not cover or crop the mockup.

## 14. No proposal board when declined
Prompt flow:
1. 「請幫我做這張包裝 mockup。」
2. User answers: 「不需要。」

Expected:
- `Proposal mode: no`;
- normal mockup only;
- no proposal information band.

## 15. Proposal intent already explicit
Prompt:
「請做成提案用的高保真名片 mockup。」

Expected:
- do not ask the proposal-use question again;
- infer `Proposal mode: yes` from the explicit request;
- include the proposal band after the mockup passes QA.
