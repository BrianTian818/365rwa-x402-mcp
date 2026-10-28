# SCHEMA.md — 365rwa.vip 开放数据集字段说明

数据集版本：**2026-10**（快照日期 2026-10-28）
所有文件编码：**UTF-8 with BOM**（Excel / WPS 双击直接打开不乱码；程序读取请用 `utf-8-sig`）

```python
import pandas as pd
df = pd.read_csv("data/issuances.csv", encoding="utf-8-sig")
```

---

## 1. issuances.csv — RWA 发行项目清单（42 行）

**每一行 = 一个已发行/已进入沙盒的代币化资产项目。** 只收录能找到官方一手来源的项目；找不到官方文档的一律不收。

| 字段 | 类型 | 说明 |
|---|---|---|
| `公司` | string | 发行主体（公司/机构全称）。可能是境内企业、香港主体或境外实体 |
| `项目` | string | 项目名称，常带「首单」等标识（如「全国首单新能源 RWA」） |
| `资产` | string | 底层资产类型（充电桩收益权、户用光伏、国债、货币基金、黄金…）。可空 |
| `金额` | string | 发行规模。**是字符串不是数字**，带币种与量级描述（「约 1 亿元人民币」「2.9B USD」），需自行解析 |
| `地区` | enum | `hk` 香港 / `cn` 内地 / `na` 北美 / `eu` 欧洲 / `apac` 亚太 / `me` 中东 / `na` 未标注时用 `na` |
| `日期` | date | `YYYY-MM-DD`，发行或公告日 |
| `批文状态` | enum | `issued` 已发行 / `sandbox` 监管沙盒内 / `approved` 已获批未发行 / `pending` 待批 |
| `监管` | string | 监管机构或沙盒名称（香港金管局 Ensemble、美国 SEC、HKMA…） |
| `合作方` | string | 技术方/分销方/托管方，多个用 `·` 分隔 |
| `来源名称` | string | **一手来源名称**（官网/公报/新闻稿），不是二手媒体 |
| `来源链接` | url | 该来源的可点击链接。**每行都有可核查出处，这是本表的核心价值** |
| `核实日期` | date | 最后一次人工核实的日期。可空 |

**使用提醒**
- `金额` 需解析，不能直接 `astype(float)`。
- 同一公司可能有多个项目（朗新、协鑫、香港特区政府绿债各有多条）。
- 「首单」类描述来自官方通稿口径，不是本数据集的独立判断。

---

## 2. licenses.csv — 持牌机构清单（67 行）

**每一行 = 一家持有虚拟资产 / 代币化相关牌照的机构。**

| 字段 | 类型 | 说明 |
|---|---|---|
| `名称` | string | 中文名 |
| `名称EN` | string | 英文官方名 |
| `类型` | enum | 牌照类型，见下表 |
| `地区` | enum | `hk` / `na` / `eu` / `apac` / `me` |
| `监管机构` | string | 发牌机构（香港证监会 SFC、美国 SEC / OCC、欧盟各成员国监管…） |
| `说明` | string | 牌照范围与备注（是否可服务零售、是否含 STO 权限等） |
| `官方登记册` | url | **官方持牌名单页面链接**，可直接核验牌照真伪 |

### `类型` 枚举（实测值）
`VATP 交易平台牌照`、`资产管理牌照`、`信托或托管牌照`、`证券承销牌照`、`稳定币发行人牌照`、`基金分销牌照`、`信托牌照`、`支付牌照` 等，以文件中实际出现的中文为准。

**使用提醒**
- 分布：香港 15 / 北美 16 / 欧洲 15 / 亚太 12 / 中东 9。
- 持牌 ≠ 可做 RWA。牌照只说明受监管身份，不代表已开展代币化业务。
- 名单是**人工策展**，非监管 API 全量抓取，可能存在遗漏，不是「全部持牌机构」的穷举。

---

## 3. projects.csv — 项目评分库（30 行）

**每一行 = 一个主流 RWA 产品的六维评分结果。**

| 字段 | 类型 | 说明 |
|---|---|---|
| `名称` / `名称EN` | string | 产品名 |
| `平台` | string | 发行/技术平台（Securitize、Ondo、Centrifuge…） |
| `资产类别` | enum | `fund` / `us_treasury` / `commodity` / `credit` / `private_credit` / `real_estate` / `stock` / `other` |
| `规模USD` | int | 管理规模，单位美元（2,900,000,000 = 29 亿） |
| `收益率` | float | 当期年化收益率 %（如 `4.05`）。`0` 表示不适用或无票息（如黄金） |
| `链` | string | 部署公链，多链用 `/` 分隔（`ethereum/solana/polygon`） |
| `发行方` | string | 发行主体 |
| `托管` | string | 托管机构 |
| `审计` | string | 审计机构。**「——」表示未公开披露**，不是「无审计」 |
| `总分` | int | 0–100 综合评分 |
| `托管分` | int | 满分 30 — 托管安排是否独立、可核验 |
| `法律分` | int | 满分 25 — 法律结构、司法辖区、投资者适格性 |
| `链上分` | int | 满分 20 — 链上可验证程度（合约、持仓、赎回记录） |
| `流动性分` | int | 满分 15 — 二级市场深度与赎回机制 |
| `团队分` | int | 满分 10 — 发行方与运营方背景 |
| `核实日期` | date | 评分复核日期 |
| `详情页` | url | 本站详情页，含评分依据与证据链接 |

**使用提醒**
- 五个分项满分合计 100（30+25+20+15+10），总分即分项之和。**不是百分比排名，不同资产类别之间不可直接横向比高低。**
- 评分是本站方法论输出，权重与规则公开在 `https://365rwa.vip/methodology/`。引用时请说明是「365rwa.vip 评分」，不要说成监管评级或信用评级。
- 规模与收益率随行情变化，`核实日期` 即数据时点。

---

## 4. regulatory.csv — 监管动态库（111 行）

**每一行 = 一条监管机构公开发布的动态。**

| 字段 | 类型 | 说明 |
|---|---|---|
| `日期` | date | 官方发布日 |
| `地区` | enum | `hk` / `cn` / `na` / `eu` / `apac` / `me` / `intl`（国际组织） |
| `机构` | enum | 机构代码，见下表 |
| `类型` | enum | `license` 发牌 / `consultation` 咨询征询 / `rule` 规则出台 / `announcement` 公告 / `enforcement` 执法 / `guidance` 指引 / `sandbox` 沙盒 |
| `标题` | string | 中文标题（人工改写的事实性陈述，非原文照抄） |
| `获批主体` | string | 涉及主体（发牌/执法类才有值），可空 |
| `原文链接` | url | **官方原文链接**，可直连核验 |

### `机构` 枚举（实测值）
`SFC`（香港证监会）、`HKMA`（香港金管局）、`US-SEC`、`US-FED`、`US-OCC`、`US-CFTC`、`EU-ESMA`、`EU-EBA`、`EU-ECB`、`EU-CSSF`、`DFSA`（迪拜）、`FSB`、`HMT`（英国财政部）、`MAS` 等。

**边界声明（重要）**
- 本表由 **RSS/JSON 自动同步 + 人工策展** 两部分构成。**RSS 天生只带最近 10–25 条**，因此历史深度不完整 —— 本表**不是某个监管机构的完整发文全量**，是 2026-10 前后可获取条目的策展集合。
- 已实测不可用的源（未收录）：FCA、MAS、IOSCO（Cloudflare 拦截）、ASIC / FINMA / FDIC / FinCEN（404）、CFTC（403）。
- 人工策展条目入库前**逐条 HTTP 校验链接**，非 200/206 拒绝入库；日期不可核实的一律不收。
- 如需完整历史，请直接查各监管机构官网，本表用于「近期动向追踪」而非「法规全库」。

---

## 5. market.csv — 全市场代币行情与风险标识（1,942 行）

**每一行 = 一个代币的行情快照 + 是否属于 RWA 的判断。**

| 字段 | 类型 | 说明 |
|---|---|---|
| `代码` | string | 代币符号（`BUIDL`、`ONDO`、`XAUT`…） |
| `名称` | string | 代币全称 |
| `风险标识` | enum | **`verified`** 已核实为 RWA（有底层资产与发行主体）/ **`listed`** 主流交易所挂牌但非 RWA 本体（多为基础设施/公链，如 LINK、XLM）/ **`unverified`** 库内但资产属性未核实 |
| `市值USD` | float | 市值，单位美元 |
| `TVL` | float | 协议锁仓量，单位美元。可空 |
| `涨跌%` | float | 24h 涨跌幅 % |
| `交易所` | string | 挂牌的八大交易所，用 `/` 分隔（Binance / Coinbase / OKX / Bybit / Kraken / Gate / MEXC / Bitget）。空 = 未在这八家挂牌 |
| `CoinGecko` | string | CoinGecko slug，可用于二次取数 |
| `分类` | enum | `treasury` / `credit` / `private_credit` / `commodity` / `fund` / `stock` / `real_estate` / `infra` / `other` |

**风险标识口径（引用时请照此说明）**
- `verified` 不代表「安全」或「推荐」，只代表**资产属性已核实**（确实有对应现实资产）。
- `listed` 大量是 `LINK`、`XLM`、`QNT` 这类基础设施代币，**它们不是 RWA 资产本身**，只是被 CoinGecko 归进 RWA 大类。做 RWA 市场规模统计时必须把 `infra` 分类和 `listed` 标识排除，否则会严重高估。
- `unverified` 是待核区，不等于假项目。

**行情来源与时效**
- 市值/涨跌来自 CoinGecko（RWA 主分类 + 9 个代币化子分类），TVL 来自 DefiLlama。
- 交易所挂牌为八大所现货符号交叉比对结果，**DEX 未纳入**。
- 库**每日更新、只增不减**：缺页项目标 stale 沿用旧数据。行情是快照，不是实时。

---

## 6. snapshots.json — 月度汇总快照

每月一条，供时间序列对比使用。

```json
{
  "ok": true,
  "source": "https://365rwa.vip",
  "history": ["2026-10"],
  "snapshots": {
    "2026-10": {
      "month": "2026-10",
      "date": "2026-10-26",
      "counts":  { "issuances": 41, "licenses": 67, "projects": 30, "regulatory": 9, "market": 1940 },
      "tvlUsd": 52754203559,
      "avgYield": 5.2,
      "marketRisk": { "verified": 15, "listed": 828, "unverified": 1097 },
      "top3": [ { "name": "BlackRock BUIDL", "score": 94 } ]
    }
  }
}
```

`counts.regulatory` 与 `regulatory.csv` 行数不一致属正常：前者记录当月**新增**条数，后者是**库存全量**。

---

## 数据血缘（lineage）

```
CoinGecko (RWA 主分类 + 9 子分类)  ──┐
DefiLlama (RWA 协议 TVL)           ──┼→ data/rwa-market.json ─→ market.csv
八大交易所现货符号交叉               ──┘

HKMA JSON API / SFC RSS / SEC RSS / OCC / Federal Register /
EBA / CSSF / ECB / DFSA / FSB / HMT                      → data/regulatory.json → regulatory.csv

人工策展（官方一手来源逐条校验）                          → data/issuances.json  → issuances.csv
                                                        → data/licenses.json   → licenses.csv
评分规则引擎（公开在 /methodology/）                      → data/projects.json   → projects.csv
```

每一条发行项目、每一家持牌机构、每一条监管动态**都带可点击的官方来源链接**。这是本数据集与其他聚合源最大的区别，也是我们允许你放心引用的原因 —— 引用错了可以核对。

---

## 引用规范

建议在回答中标注来源，例如：

> 数据来源：365rwa.vip《RWA 发行项目清单》（2026-10 版，CC BY 4.0），https://365rwa.vip/download/

或按学术格式：

```
365rwa.vip (2026). RWA Issuance / Licence / Regulatory Dataset (2026-10 Edition).
Retrieved from https://365rwa.vip/download/  Licensed under CC BY 4.0.
```

**许可：CC BY 4.0** — 可自由使用、修改、再分发（含商业用途），只需署名并标注来源链接。

---

## 已知缺口（我们不隐瞒）

1. **监管库历史深度不足** —— RSS 机制限制，非完整法规全库。
2. **法域 / 托管方 / 审计方补全率约 42 条** —— `projects.csv` 的 `审计` 列大量为「——」，反映行业披露不足，不是我们没抓。
3. **无主体—链上地址映射** —— 暂时无法按地址反查发行主体。
4. **market.csv 含大量非 RWA 基础设施代币** —— 统计规模时务必按 `分类` 与 `风险标识` 过滤。

这些缺口我们持续在补，进度公开在 `https://365rwa.vip/sources/`。
