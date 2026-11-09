# Edge Preservation Guide

Use this reference when the artwork contains any design element close to a trim edge.

## What counts as edge-adjacent content

- border lines;
- full-height or full-width color stripes;
- keylines around the card/package face;
- artwork intentionally aligned to the edge;
- logos or text placed near the trim;
- full-bleed blocks whose visibility at the face edge matters.

## Common failure modes

1. **Stripe mistaken for thickness**
   A printed face stripe on a business card vanishes because the scene renders only the exposed paper edge.

2. **Border clipped by framing**
   Automatic perspective or crop places the artwork too tight and cuts off a thin border.

3. **Trim edge swallowed by shadow or occlusion**
   Lighting or overlap hides a thin but important edge line.

4. **Over-naturalization**
   Surface shading/texture makes a thin line disappear or appear broken.

## Prevention rules

- Prefer `contain` unless the user explicitly asked for cover/full bleed.
- When choosing or generating a card angle, keep enough of the face visible to show thin edge elements.
- For very thin lines/stripes, favor slightly stronger face visibility over dramatic perspective.
- Keep material texture subordinate so it does not eat thin rules or keylines.
- If the card overlaps another object, avoid overlap on the side that contains critical edge-adjacent content.

## Business card specific guidance

If the front face design includes a left-side brand stripe:
- the stripe must remain visible on the front face;
- the paper thickness may also be visible, but it cannot replace the stripe;
- if overlap/shadow competes with the stripe, reduce the overlap/shadow or adjust angle.

## QA interpretation

Fail the render if:
- an original border/stripe/keyline disappears without explicit crop authorization;
- a trim-edge graphic becomes partly hidden for no physical reason;
- the front-face stripe is replaced only by card thickness;
- edge-adjacent content is materially less visible than intended.

## Prompting/generation guidance for blank mockups

When generating a blank business-card substrate scene, prefer:
- a modest oblique angle rather than an extreme edge-on view;
- enough front-face area visible on all critical edges;
- soft shadows;
- realistic thickness;
- restrained texture.
