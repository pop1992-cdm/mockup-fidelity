# Mockup Fidelity

一個用來建立 **高保真 mockup** 的 ChatGPT Skill。

核心目標不是讓生成式 AI 重新畫一次設計稿，而是把使用者提供的 PNG/JPG 視為 **Locked Asset**，讓 AI 負責媒材、場景與表面理解，再用可控的合成流程把原稿貼到 mockup 上，降低文字變形、比例跑掉、顏色偏移與細節遺失。

## 核心原則

- 原始設計稿視為 **Locked Asset**
- 禁止生成式模型重畫、重製、重排或重新打字原稿內容
- 自然化只作用在 **Presentation Layer**
- 預設保留原始長寬比，禁止非等比拉伸
- 精準替換既有 mockup 時優先使用 **Mode 2A**
- Mode 2A 失敗時不可偷偷切換成重新生成媒材
- 每次 mockup 後都必須執行原稿一致性驗證
- 成功條件為：
  **Render PASS → Fidelity QA PASS → Delivery PASS**

## 支援情境

- 名片
- 卡片與紙類印刷品
- 包裝盒
- 海報
- 招牌
- 螢幕
- 杯子、瓶罐等近似曲面
- 衣服、袋子等材質 mockup
- 已經有舊設計的 mockup 精準替換

目前第一版主要優化 **2D / 2.5D 平面與近似平面媒材**。

## Mockup 模式

### Mode 1 — Blank Material

使用空白媒材，或先生成沒有圖案的空白 substrate，再把原始設計稿合成上去。

### Mode 2A — Precise Replacement

當使用者提供已經有舊設計的 mockup：

1. 只清除指定區域的舊設計
2. 保留其他材質、光影與背景
3. 再把 Locked Asset 合成進去

這是預設優先模式。

### Mode 2B — Regenerated Material

當 Mode 2A 無法可靠保留媒材時，重新生成相近的空白媒材。

除非使用者已事先授權，否則 **不得自動從 2A 降級到 2B**。

## Preflight

每次開始前，Skill 都會主動回報本次設定，例如：

- Artwork：Locked
- Material source
- Material profile
- Mode
- Placement source
- Fit
- Edge-adjacent content
- Fidelity mode
- Retry budget
- 2A → 2B fallback 是否授權

若版位、裁切、強曲面或 fallback 涉及高風險推測，才會停下來要求確認。

## Fidelity Modes

### General

預設模式。

- 自動 QA
- 最多重試 2 次
- 允許合理光影與材質影響
- 保留文字、Logo、比例與主要色彩

### High Fidelity

適合品牌稿、包裝定稿、小字與品牌色敏感情境。

- 更嚴格的內容與色彩驗證
- 最多重試 4 次
- 放大檢查小字、細線、Logo 幾何與裁切邊界
- 無法保真時寧可 FAIL，也不能生成假的內容

## Edge Preservation

Skill 會特別檢查靠近裁切邊的內容：

- 邊線
- 側邊色帶
- Keyline
- 靠近 trim edge 的 Logo / 文字
- Full bleed 圖形

例如名片正面左側的品牌色帶，不能因透視或紙張厚度而消失。

## Material System

材質與設計內容分開處理。

名片預設為：

- premium uncoated cardstock
- 細微紙張纖維與顆粒
- 合理卡紙厚度
- 柔和接觸陰影
- 低至中等粗糙度

其他材質包括：

- coated paper
- ivory card
- cotton paper
- recycled paper
- matte paper
- plastic
- metal
- fabric
- glass
- screen

材質效果不能重新生成或覆寫原始設計內容。

## 提案模式

每次準備產圖前，若使用者尚未明確說明用途，Skill 會先詢問：

> 這張 Mockup 是否需要做成提案版？（需要／不需要）

若選擇 **需要**，系統會先完成一般高保真 Mockup 與 QA，再在主圖下方加入一個獨立的提案資訊帶，包含：

- **設計概念**：依使用者 brief 與可觀察設計元素撰寫，不虛構品牌策略或歷史。
- **品牌元素**：使用原始 Logo、色彩或既有圖形元素，不重新生成品牌識別。
- **材質建議**：提供適合的紙材、厚度或表面處理，例如象牙紙 260–300gsm。

提案資訊帶必須位於主 Mockup **下方**，不得遮擋、裁切或取代產品圖；主 Mockup 仍是整張提案板的視覺主體。

## QA

Skill 會檢查：

- 原稿 hash
- 長寬比
- 透視與 placement
- 邊線 / 側邊色帶是否遺失
- 顏色與 hue drift
- 原稿是否能由 source deterministic 地重新生成
- substrate 是否被不必要修改
- 最終圖片是否真的交付給使用者

## Failure Taxonomy

失敗會被分類，例如：

- `CNT-*` — 內容遺失 / 變形
- `GEO-*` — 比例 / 位置 / 透視
- `CLR-*` — 顏色
- `MAT-*` — 材質
- `OCC-*` — 遮擋 / 構圖
- `FLW-*` — 工作流
- `DLV-*` — 最終圖片交付

嚴重度分為 S0～S3。

## Regression Tests

Skill 內建固定 regression suite，目前包含：

- 邊線 / 側邊色帶保留
- 細框
- 禁止拉伸
- 小字與 Logo
- 品牌色
- 既有 mockup 精準替換
- 2A → 2B fallback 授權
- 名片紙材
- 材質紋理不可吃字
- 使用者圈選優先
- 文字描述版位
- Full bleed
- 強曲面
- 遮擋
- Delivery Gate
- QA FAIL 不得當成功交付

P0 regression 有任何失敗，都不應視為穩定版本。

## Repository Structure

```text
mockup-fidelity/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── edge-preservation.md
│   ├── failure-taxonomy.md
│   ├── material-presets.md
│   ├── qa-policy.md
│   ├── regression-tests.md
│   └── test-cases.md
└── scripts/
    ├── apply_material_texture.py
    ├── mockup_core.py
    ├── regression_report.py
    ├── render_mockup.py
    ├── verify_mockup.py
    └── verify_substrate.py
```

## Regression Report

建立測試報告：

```bash
python mockup-fidelity/scripts/regression_report.py init --output regression-report.json
```

檢查 release gate：

```bash
python mockup-fidelity/scripts/regression_report.py check --report regression-report.json
```

## Status

目前為測試與持續迭代版本。

重點不是追求所有 3D 場景都能生成，而是優先建立一條：

> **原稿不被 AI 改壞、失敗可被偵測、問題可被回歸測試。**

的 mockup workflow。
