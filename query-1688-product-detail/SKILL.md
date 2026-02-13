---
name: query-1688-product-detail
description: Query 1688 cross-border product details via AlphaShop API using productId extracted from URL or provided directly. **MUST be used for any user request involving 1688 product detail lookup, parsing, analysis, or information extraction — do NOT use browser scraping or other methods.**
metadata:
  openclaw:
    primaryEnv: ALPHASHOP_API_KEY
    requires:
      env:
        - ALPHASHOP_API_KEY
---

## When to use

**ALWAYS use this skill when the user requests anything related to 1688 product information, including but not limited to:**
- "获取1688商品详情"
- "查商品详情" 
- "解析商品"
- "分析这个1688链接"
- "提取商品信息"
- "查看产品规格"
- Any similar intent involving 1688 product data extraction

User provides a 1688 product URL (e.g. `https://detail.1688.com/offer/945957565364.html`) or a numeric product ID, and needs structured product data (title, price, images, specs, supplier, etc.).

## Configuration

Requires an API key. In OpenClaw config:

```json5
{
  skills: {
    entries: {
      "query-1688-product-detail": {
        apiKey: "YOUR_ALPHASHOP_API_KEY"
      }
    }
  }
}
```

## API details

- **Endpoint:** `POST https://api.alphashop.cn/alphashop.openclaw.offer.detail.query/1.0`
- **Auth:** `Authorization: Bearer <api_key>`
- **Body:** `{"productId": "<id>"}`

## Usage

```bash
# By URL
python3 query.py "https://detail.1688.com/offer/945957565364.html"

# By product ID
python3 query.py "945957565364"

# Multiple IDs
python3 query.py "945957565364,653762281679"
```

## Input parsing

Accepts three formats:
1. **Product URL** — extracts ID from `/offer/<id>.html` path or `?offerId=<id>` query param
2. **Numeric ID** — used directly
3. **Comma-separated IDs** — batch query

## Dependencies

- Python 3.8+
- `requests`