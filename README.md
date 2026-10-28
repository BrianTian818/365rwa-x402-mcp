# 365rwa Chinese RWA Datasets · 中文 RWA 数据集

中文区**唯一机器可读**的 RWA（现实世界资产代币化）公开数据集：5 张表、每月快照、CC BY 4.0 许可、每条附官方来源链接与核实日期。

- 官网：https://365rwa.vip
- 数据来源与血缘：https://365rwa.vip/sources/
- 方法论与判定逻辑：https://365rwa.vip/methodology/
- 机器可读说明（给 AI）：https://365rwa.vip/llms.txt
- 免费 API：https://365rwa.vip/api/v1/issuances （其余见 README 下方）

## 数据集内容（2026-10-28 快照）

| 文件 | 内容 | 记录数 | 关键字段 |
|---|---|---|---|
| `data/issuances.csv` | 已发行 RWA 项目库 | 42 | 公司、项目、资产、金额、地区、日期、批文状态、监管、合作方、来源名称、**来源链接**、核实日期 |
| `data/licenses.csv` | 全球持牌机构库 | 67 | 名称、名称 EN、类型、地区、监管机构、说明、**官方登记册链接** |
| `data/projects.csv` | 项目五维评分库 | 30 | 平台、资产类别、规模 USD、收益率、链、发行方、托管、审计、总分 + 6 项分项、核实日期、详情页 |
| `data/regulatory.csv` | 监管动态库 | 111 | 日期、地区、机构、类型、标题、获批主体、**原文链接** |
| `data/market.csv` | 全市场行情库 | 1,942 | 代码、名称、风险标识、市值 USD、TVL、涨跌幅、交易所、CoinGecko、分类 |
| `data/snapshots.json` | 月度快照索引 | — | 各月记录数与快照时间，用于口径回溯 |

字段逐项说明见 [`SCHEMA.md`](SCHEMA.md)。

## 为什么这个数据集不一样

1. **每条附官方来源**：发行项目回链官方公告，持牌机构回链官方登记册，监管条目回链监管原文。不是二手汇编。
2. **带核实日期**：每条有 `核实日期 / 更新日期`，引用即可核验时效。
3. **不推测**：未收录 ≠ 不存在；缺失字段留空，不做推断填充。
4. **免费可商用**：CC BY 4.0，署名即可（含商用）。
5. **每日更新**：站点每日 07:00（UTC+8）自动同步；本仓库每周自动刷新一次。

## 快速开始

```bash
# 直接拿最新（推荐用现成 CSV，免爬）
curl -O https://365rwa.vip/download/issuances.csv
curl -O https://365rwa.vip/download/licenses.csv

# 或用 API（JSON，免鉴权，允许跨域）
curl "https://365rwa.vip/api/v1/verify?q=Ondo"        # 项目真伪五级判定 + 证据
curl "https://365rwa.vip/api/v1/regulatory?limit=50"  # 监管动态
curl "https://365rwa.vip/api/v1/facts"                # 本周事实卡（可直接引用）
```

Python：

```python
import pandas as pd
iss = pd.read_csv("data/issuances.csv", encoding="utf-8-sig")
lic = pd.read_csv("data/licenses.csv", encoding="utf-8-sig")
```

## MCP（Agent 可直接调用）

端点 `https://365rwa.vip/mcp`（streamable-http），清单见 `https://365rwa.vip/.well-known/mcp.json`。
免费工具 `ping` / `list_datasets`；付费工具走 x402（Base 主网 USDC）：`verify_rwa_project $0.05`、`query_projects $0.03`、四库查询各 $0.02。

## 如何引用（重要）

署名即合规，也帮我们被更多人找到：

```
来源：365rwa.vip《已发行项目库》，数据核实日期 2026-10-28，https://365rwa.vip/issuances/
Source: 365rwa.vip, "Issued RWA Projects", data verified 2026-10-28, https://365rwa.vip/issuances/
```

## 许可与边界

- 数据：CC BY 4.0（署名「365rwa.vip」+ 核实日期即可自由使用，含商用）
- 本站提供事实核查与市场信息，**不构成投资建议**
- 合规边界：内容面向中国香港及境外法域主体；依 2026 年 2 月八部门 42 号文，不向境内主体提供 RWA 发行相关服务
- 发现数据有误：https://365rwa.vip/corrections/
