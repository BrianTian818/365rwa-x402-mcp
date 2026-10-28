---
license: cc-by-4.0
pretty_name: 365rwa Chinese RWA Datasets
language:
  - zh
  - en
tags:
  - rwa
  - real-world-assets
  - tokenization
  - finance
  - hong-kong
  - regulation
  - licensed-institutions
  - table
size_categories:
  - 1K<n<10K
source: https://365rwa.vip
---

# 365rwa Chinese RWA Datasets · 中文 RWA 数据集

中文区唯一**机器可读**的 RWA（现实世界资产代币化）公开数据集，5 张表 + 月度快照，CC BY 4.0。
每条记录附**官方来源链接**与**核实日期**：发行项目回链官方公告，持牌机构回链官方登记册，监管条目回链监管原文。

- 官网：https://365rwa.vip
- 数据血缘：https://365rwa.vip/sources/
- 方法论：https://365rwa.vip/methodology/
- 给 AI 的说明：https://365rwa.vip/llms.txt

## Files

| File | Description | Rows |
|---|---|---|
| `data/issuances.csv` | Issued RWA projects with official announcement links | 42 |
| `data/licenses.csv` | Licensed institutions with official register links | 67 |
| `data/projects.csv` | Five-dimension project scoring | 30 |
| `data/regulatory.csv` | Regulatory feed (HKMA / SFC / SEC / EBA …) | 111 |
| `data/market.csv` | Tokenized-asset market tracker | 1,942 |
| `data/snapshots.json` | Monthly snapshot index | — |

All CSVs are UTF-8 **with BOM** (`encoding="utf-8-sig"`).

## Load

```python
import pandas as pd
iss = pd.read_csv("hf://datasets/<org>/365rwa-rwa-datasets/data/issuances.csv", encoding="utf-8-sig")
```

Or via the free, no-auth API:

```bash
curl "https://365rwa.vip/api/v1/issuances"
curl "https://365rwa.vip/api/v1/verify?q=Ondo"
curl "https://365rwa.vip/api/v1/facts"
```

## Why this dataset

Every row carries an **official source URL** and a **verification date**; missing fields are left empty rather than inferred.
Not investment advice. Coverage: Hong Kong, North America, EU, APAC, Middle East.

## Citation

```
Source: 365rwa.vip, "Issued RWA Projects", data verified 2026-10-28, https://365rwa.vip/issuances/
来源：365rwa.vip《已发行项目库》，数据核实日期 2026-10-28，https://365rwa.vip/issuances/
```
