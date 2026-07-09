# Data-Driven Ecommerce Diagnosis Reference

Use this reference only when the user provides reviews, VOC, competitor data, or funnel metrics.

## Data Mapping

### Buyer Review Fields

Common columns and aliases:

- `review_text`: 评价内容, 评论内容, 买家评价, content, text
- `rating`: 星级, 评分, score, stars
- `review_time`: 评价时间, time, date
- `sku`: 规格, 颜色, 款式, sku_name
- `sentiment`: 情感, 正负面, positive/negative
- `tags`: 评价标签, 印象词, 系统标签
- `images`: 买家秀, 图片数, has_image
- `followup`: 追评, 追加评价

If rating is absent, infer sentiment cautiously from text and label it as inferred.

### VOC Fields

Common columns:

- `question`: 问大家, 咨询问题, 客服问题
- `answer`: 回答, 客服回复
- `topic`: 主题, 分类
- `count`: 次数, 频次
- `refund_reason`: 退款原因, 售后原因

### Competitor Fields

Common columns:

- `competitor_name`: 竞品名, 店铺名, brand
- `price`: 价格, 到手价
- `sales`: 销量, 已售, GMV rank
- `rating`: 评分
- `review_count`: 评价数
- `main_claim`: 主卖点, 标题卖点
- `image_notes`: 主图内容, 画面结构
- `negative_themes`: 差评主题
- `proof`: 认证, 检测, 质保, 背书
- `url`: 链接

### Funnel Fields

Common columns:

- `impressions`, `曝光`, `展现`
- `clicks`, `点击`
- `ctr`, `点击率`
- `add_to_cart_rate`, `加购率`
- `conversion_rate`, `转化率`, `CVR`
- `refund_rate`, `退款率`
- `traffic_source`, `渠道`, `流量来源`

## Review/VOC Analysis Procedure

1. Normalize text: remove duplicates, split follow-up reviews, keep SKU context.
2. Cluster themes into purchase motivation, praise, complaint, hesitation, usage scenario, expectation mismatch.
3. Estimate frequency using counts when available. If counts are absent, use qualitative ranking and say so.
4. Extract buyer language that can become compliant image copy.
5. Compare image claims against review reality:
   - If image promises a benefit that reviews complain about, flag P0 or P1.
   - If reviews repeatedly praise a benefit not shown in the image, flag P1 opportunity.
   - If users ask the same pre-sale question, move that answer into main image/detail first screen.

## Competitor Analysis Procedure

Compare the seller against 3-5 closest competitors when available:

- Category role: low-price, brand trust, functional upgrade, appearance/design, niche scenario
- Thumbnail strategy: product size, text count, price visibility, scene vs white background
- Claim strategy: main claim, proof claim, promo claim, risk claim
- Trust strategy: logo, warranty, certifications, reviews, sales proof
- Weakness from competitor reviews: complaints that the seller can answer visually

Output competitor gaps as:

- `must_match`: baseline proof or information buyers expect in the category
- `differentiate`: angle the seller can own
- `avoid`: overused or risky competitor claim pattern

## Funnel Interpretation

Use data to choose the likely bottleneck:

- Low CTR + normal CVR: main image/title/search-card problem.
- Normal CTR + low CVR: detail page, price trust, proof, SKU, or review mismatch problem.
- High add-to-cart + low purchase: price, coupon, shipping, warranty, payment friction, or final trust problem.
- High refund/negative-review rate: expectation control and claim accuracy problem.
- Paid traffic weak but organic normal: audience/keyword mismatch or creative mismatch.

Do not infer causality from one metric alone. State likely causes and what additional data would confirm them.

## Evidence-Weighted Scoring Rubric

Use this when data beyond images is provided:

### Visual Conversion Readiness, 35

- Product and scenario clarity: 10
- Selling point hierarchy: 10
- Thumbnail readability: 8
- Price/promo framing: 4
- Mobile platform fit: 3

### Review/VOC Alignment, 25

- Top praise reflected in image/detail page: 7
- Top complaints answered or expectation-controlled: 8
- High-frequency questions answered before purchase: 5
- Buyer language used accurately: 3
- SKU-specific issues handled: 2

### Competitor Differentiation, 20

- Clear defendable difference: 7
- Matches category baseline proof: 5
- Avoids competitor sameness: 4
- Uses competitor weaknesses as opportunity: 4

### Trust And Proof Completeness, 10

- Proof for numerical/efficacy claims: 4
- Warranty/after-sales clarity: 3
- Authentic product/detail evidence: 3

### Compliance And Expectation Control, 10

- No absolute or unverifiable claims: 4
- Sensitive claims have support: 3
- Copy does not create unrealistic usage expectations: 3

## Recommended Output Snippets

For each recommendation, prefer this format:

- Evidence: “差评中多次出现‘声音大’，但主图写的是‘久吹舒适’，没有解释噪音档位。”
- Impact: “用户收到货后预期落差会增加差评和退款。”
- Fix: “把主图副卖点改为‘8档风速可调’，详情页补不同档位噪音/适用场景；没有实测数据时不要写静音分贝。”

For copy hierarchy, provide:

- Main headline: one primary buyer benefit
- Sub headline: one proof-backed feature
- Three badges max: parameter, service, scenario
- Risk control: remove or soften unsupported claims
