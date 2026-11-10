# Proposal Mode

Use this reference only when `Proposal mode: yes`.

## Goal

Turn the finished mockup into a presentation-ready proposal board while keeping the high-fidelity mockup itself unchanged.

The reference composition is:
- large mockup image in the upper/main area;
- a separate horizontal information band beneath it;
- three clearly separated sections: `設計概念`, `品牌元素`, `材質建議`.

## Mandatory sections

### 1. 設計概念

Write 2–4 short lines.

Source hierarchy:
1. user's explicit brief;
2. visible artwork features;
3. observable brand colors/shapes/layout.

Do not invent:
- brand history;
- strategic positioning;
- emotional symbolism;
- market claims;
- design rationale not supported by the brief or visuals.

Good pattern:
`以「信任、專業、連結」為核心。延伸品牌幾何語彙，透過留白與重複曲線建立一致的中英文視覺節奏。`

Only use concepts like the above when supported by user input or clearly observable design cues.

### 2. 品牌元素

Show source-derived brand material:
- exact source logo/mark;
- exact source colors;
- a crop/extraction of an existing shape;
- a deterministic combination of existing shapes.

Optional relationship graphic:
`原始品牌元素 → 延伸圖形`

Do not redraw the source logo or silently create a new logo.
If the extension would require invention, show color swatches or extracted shapes instead.

### 3. 材質建議

Recommend one primary substrate/finish and optionally one alternate.

Format:
`[材質名稱]（[spec]）`
`[one-line reason]`

Examples:
- `象牙紙（260–300gsm）` — 細緻紙紋、溫潤觸感，適合專業名片。
- `高級未塗佈卡紙（300–350gsm）` — 低反光、觸感自然，適合簡約品牌。
- `霧膜銅版紙（250–300gsm）` — 表面平整、色彩飽和，適合照片與高彩度視覺。

Use `material-presets.md` for the physical recommendation.

## Layout

- Main mockup: roughly 75–85% of total visual height.
- Proposal band: roughly 15–25% of total height.
- Three columns with clear vertical separation.
- Use a neutral light background or source-derived subtle tint.
- Keep headings compact and high-contrast.
- Use small supporting visuals only.
- Keep the product/mockup as the visual hero.

## Fidelity rule

The proposal band is a presentation layer. It must never be merged into or used to regenerate the locked artwork.

Recommended sequence:
1. Render locked-artwork mockup.
2. Run fidelity QA.
3. Freeze the passing mockup.
4. Add proposal band beneath it.
5. Run proposal-layout QA.
6. Deliver the combined board.

## Proposal QA

PASS only when:
- user chose proposal mode;
- all three sections appear;
- no unsupported claims are invented;
- brand visuals are source-derived;
- material recommendation is plausible;
- proposal panel does not obscure/crop the mockup;
- the main mockup remains the dominant visual.

If the user chose `no`, the proposal band must not appear.
