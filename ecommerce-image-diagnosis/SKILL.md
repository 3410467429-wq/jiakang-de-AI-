---
name: ecommerce-image-diagnosis
description: >-
  电商主图、详情页、搜索结果与转化素材诊断助手。Use when the user provides product images,
  detail page screenshots, search/listing screenshots, product links, buyer
  reviews, VOC/差评数据, 问大家内容, 客服咨询记录, conversion metrics, or competitor
  data and asks for 主图诊断、详情页诊断、商品图分析、主图优化、竞品对比、评价驱动优化、转化率诊断,
  ecommerce image diagnosis. Supports Taobao, Tmall, Pinduoduo, Douyin, JD and
  similar ecommerce platforms.
---

# 电商主图&详情页诊断 Skill

## Core Rule

Diagnose from the strongest available evidence. Do not stop at visual taste when the user provides reviews, VOC, conversion data, or competitor data. Tie each recommendation to one of:

- visual evidence from the image/screenshot
- buyer review or VOC evidence
- competitor gap evidence
- platform compliance risk
- conversion funnel data

If data is missing, perform a partial diagnosis and clearly label assumptions.

## Accepted Inputs

Use any combination of:

- Product main images, detail page screenshots, search/listing screenshots, SKU images
- Product link or platform context
- Buyer reviews: positive reviews, negative reviews, review tags, ratings, review counts, follow-up reviews
- VOC sources: 问大家, 客服咨询, refund reasons, live-stream comments, product Q&A
- Competitor data: competitor images, selling points, price, rating, review count, sales rank, negative-review themes, detail page structure
- Funnel data: impressions, CTR, clicks, add-to-cart rate, conversion rate, refund rate, traffic source, A/B test results

When files are spreadsheets or CSVs, inspect columns first and map them to the schemas in `references/data_driven_diagnosis.md`.

## Workflow

### 1. Classify Materials

Identify which evidence groups are present:

- `image_only`: images/screenshots only
- `review_enriched`: images plus buyer reviews/VOC
- `competitor_enriched`: images plus competitor data
- `data_full`: images plus reviews/VOC plus competitor/funnel data

Proceed with partial diagnosis if only one group is present.

### 2. Extract Product And Claim Inventory

From the image and provided text, list:

- Product category, brand, price band, target user and likely platform
- Visible selling points and their hierarchy
- Numerical claims, efficacy claims, medical/health claims, absolute words, certification claims
- Trust signals: brand, warranty, certifications, test reports, sales proof, reviews, after-sales promises

Mark claims as:

- `verified`: backed by provided data or proof
- `unverified`: visible but unsupported
- `risky`: likely to trigger compliance or refund expectation risk

### 3. Analyze Review/VOC Data When Provided

Read `references/data_driven_diagnosis.md` when review or VOC data is present.

Extract:

- Top purchase motivations
- Top praise themes
- Top complaint themes
- Top hesitation/questions before purchase
- Mismatch between image promises and buyer feedback
- Words buyers actually use to describe value

Prioritize image/detail page improvements that address high-frequency complaints or high-intent questions.

### 4. Analyze Competitor Data When Provided

Read `references/data_driven_diagnosis.md` when competitor data is present.

Compare:

- First-screen visual strategy
- Product occupancy and thumbnail readability
- Main selling point sequence
- Price/value framing
- Trust proof density
- Compliance risk level
- Review strengths and weaknesses

Do not recommend copying competitors. Identify defendable differentiation and missing proof.

### 5. Score Dynamically

If only image material is provided, score main image or detail page on the original 100-point visual framework:

Main image:
- Visual clarity: 20
- Information delivery: 25
- Differentiation: 20
- Trust: 20
- Compliance: 15

Detail page:
- First-screen impact: 25
- Information structure: 25
- Scenario presentation: 20
- Trust proof: 20
- Conversion promotion: 10

If review/VOC and competitor data are also provided, use this 100-point evidence-weighted score:

- Visual conversion readiness: 35
- Review/VOC alignment: 25
- Competitor differentiation: 20
- Trust and proof completeness: 10
- Platform compliance and expectation control: 10

If funnel data is provided, explain whether the symptom is likely CTR, CVR, price trust, claim trust, or after-sales expectation. Use funnel data to adjust priority, not to invent causality.

### 6. Generate Findings

Write concise, concrete findings. Each major finding should include:

- Evidence: what image/data/competitor signal shows
- Impact: CTR, CVR, refund risk, compliance risk, or trust loss
- Fix: specific visual or copy change

Avoid generic advice such as “make it cleaner” unless paired with a concrete edit.

### 7. Priority Actions

Use these priority rules:

- P0: compliance risk, unverifiable claims, severe thumbnail unreadability, image promise contradicted by reviews, major refund/complaint driver
- P1: high-frequency review/VOC issue not answered on the image/detail page, missing competitor-level proof, unclear main selling point hierarchy
- P2: A/B testing, longer-term detail page order, secondary visual polish, seasonal or platform-specific variants

### 8. Output Format

Default to producing an HTML report for every diagnosis unless the user explicitly asks for chat-only output. Use Chinese unless the user asks otherwise.

Always do this sequence:

1. Build a complete diagnosis JSON with score, evidence overview, findings, and priority actions.
2. Write the JSON into the current session `work` directory.
3. Run the bundled report generator.
4. Return a short chat summary plus a link to the generated HTML file.

The chat response should stay brief:

1. 一句话结论：grade + score + biggest blocker
2. P0 优先行动摘要
3. HTML 报告链接

Run:

```bash
python <skill_dir>/scripts/generate_report.py <diagnosis_json_file> [output_html_file]
```

Use the active environment's real Python interpreter. In Codex Desktop on Windows, if `python` resolves to the Windows Store alias, call `codex_app.load_workspace_dependencies` and use the returned Python executable path. If `output_html_file` is omitted, the script writes a UTF-8 HTML report to the current Codex session `outputs` directory. The script is Codex-oriented and must not depend on WorkBuddy paths, WorkBuddy Python runtimes, or `present_files`.

Use these JSON keys when available:

- `product_name`, `platform`, `diagnosis_date`, `overall_score`, `overall_grade`, `conclusion`
- `evidence_overview`: `{ "used": [], "missing": [], "notes": "" }`
- `key_findings`: strings or objects with `title`, `evidence`, `impact`, `fix`
- `priority_actions`: `{ "P0": [], "P1": [], "P2": [] }`
- `main_image`, `detail_page`, `evidence_weighted_score`, `search_competition`, `copy_hierarchy`

If the script fails, inspect and patch the bundled script rather than falling back to stale WorkBuddy code.

## Evidence Discipline

- Do not fabricate review counts, sales, certifications, test results, lab data, or competitor metrics.
- Do not claim “best”, “first”, “guaranteed”, medical effects, antibacterial percentages, or quantified efficacy unless the user provides proof.
- Treat buyer reviews as directional evidence, not absolute truth. Mention sample limitations when the dataset is small or filtered.
- When data conflicts, prefer observed buyer feedback and funnel outcomes over seller intent.
