# Material Presets

Use this reference to give mockups believable physical material without altering locked artwork.

## General rule

Material realism belongs to the substrate and presentation layers. Do not regenerate or repaint artwork to simulate texture.

## Business card / name card

Default when unspecified:
- material: premium uncoated cardstock;
- finish: matte / uncoated;
- paper color: neutral white to warm white, based on scene lighting;
- visible texture: subtle fiber/grain, not noisy;
- edge: visible paper thickness when camera angle exposes the edge;
- light interaction: diffuse, soft highlights, low specular reflection;
- shadow: soft contact shadow where card meets surface.

Avoid:
- perfectly smooth plastic-looking white;
- strong random noise over printed artwork;
- glossy lamination unless requested;
- exaggerated fibers that compete with typography.

Optional user intents:
- "銅版紙 / coated" → smoother coated paper, slightly tighter highlights.
- "象牙卡 / ivory card" → warmer tone, fine tooth.
- "再生紙 / recycled" → visible flecks and irregular fibers, restrained.
- "棉紙 / cotton paper" → soft tooth/fiber, premium tactile appearance.
- "霧膜 / matte laminated" → smooth matte laminate, subtle soft reflections.
- "亮膜 / glossy laminated" → stronger specular highlights; mark color evaluation as lighting-sensitive.
- "壓紋紙 / embossed paper" → directional or patterned texture in substrate; keep printed artwork source unchanged.

## Poster / print

Default:
- coated or semi-matte paper;
- subtle paper wave only if scene supports it;
- preserve flat print geometry unless the physical poster bends.

## Paper packaging

Default:
- paperboard/cardboard appropriate to object;
- visible cut/fold edges;
- slight fiber texture;
- creases belong to geometry/presentation, not artwork content.

## Plastic

Default:
- smooth molded surface;
- material highlights/reflections on presentation layer;
- do not tint artwork hue unless caused by transparent/translucent substrate and user accepts it.

## Metal

Default:
- specular highlights and environment reflections;
- artwork remains source-derived;
- if printing/engraving method is not specified, use printed ink appearance rather than inventing emboss/deboss.

## Fabric

Default:
- visible weave/fibers and folds;
- artwork follows geometry through deterministic/geometry warp;
- high risk when folds are deep or logo/text crosses occlusion.

## Glass

Default:
- transparency/refraction is high risk;
- preserve artwork content and report limitations;
- never regenerate text/logo to simulate refraction.

## Screen

Default:
- no paper/fabric texture;
- preserve pixel-sharp artwork;
- optional mild screen glare belongs to presentation layer.

## Generative blank-substrate prompt pattern

When generating the material/background only, describe:
- object and viewpoint;
- physical material and finish;
- realistic lighting/shadow;
- explicitly **blank/unprinted** surface;
- no text;
- no logo;
- no illustration;
- no watermark;
- no decorative placeholder graphics.

Then composite the user's locked artwork afterward.
