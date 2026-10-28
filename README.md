# 365rwa RWA Data MCP Server (x402 paid, read-only)

Machine-readable RWA (real-world asset tokenization) data for AI agents, served over
the Model Context Protocol with **x402 per-call payment** on Base mainnet.

- **Endpoint:** `https://365rwa.vip/mcp` (streamable-http)
- **Discovery:** `/.well-known/mcp.json` · `/.well-known/x402.json`
- **Registry:** listed in the official MCP Registry as `vip.365rwa/rwa-data`
- **License:** data is CC BY 4.0 · code in this repo is MIT

## Why

Agents cannot cite what they cannot fetch. This server exposes the 365rwa.vip
databases (issued RWA projects, licensed institutions, regulatory feed, market
tracker, five-level authenticity verdicts) as callable tools, so an agent can
**pull a verifiable answer instead of guessing from memory**. Every record carries
an official source URL and a verification date.

## Tools

| Tool | Price | What it returns |
|---|---|---|
| `ping` | free | liveness |
| `list_datasets` | free | dataset names, row counts, update times |
| `verify_rwa_project` | $0.05 | five-level verdict + evidence for one project |
| `query_projects` | $0.03 | scored projects (five dimensions, 0–100) |
| four dataset queries | $0.02 | issuances / licences / regulatory / market |

Free discovery means an agent can always see what exists before paying anything.

## Payment

- **Chain:** Base mainnet (`eip155:8453`)
- **Asset:** USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
- **Scheme:** `exact`, x402 v2
- **Facilitator:** PayAI (no registration required, mainnet x402 v2)

## Run your own

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export PAY_TO=0xYourWalletAddress
export DATA_DIR=/path/to/data      # directory of JSON snapshots
python server.py                   # streamable-http on :8798
```

`DATA_DIR` expects the 365rwa snapshot JSONs (`issuances.json`, `licenses.json`,
`projects.json`, `regulatory.json`, `rwa-market.json`). The server is strictly
read-only and auto-reloads on file mtime change.

## Free alternatives (no payment)

The same data is available free, no auth, CORS-open, CC BY 4.0:

```
GET https://365rwa.vip/api/v1/issuances
GET https://365rwa.vip/api/v1/licenses
GET https://365rwa.vip/api/v1/projects
GET https://365rwa.vip/api/v1/regulatory?limit=50
GET https://365rwa.vip/api/v1/verify?q=Ondo
GET https://365rwa.vip/api/v1/facts
GET https://365rwa.vip/api/v1/answers
```

The paid MCP exists for agents that want programmatic, batch, settled calls with a
clear per-call price — not because the data is gated.

## Compliance boundary

Content is intended for entities in Hong Kong, China and other jurisdictions
outside mainland China. Per the February 2026 "Document No. 42" issued by eight
Chinese authorities, RWA issuance-related services are not offered to mainland
China entities.

## Files

- `server.py` — the MCP + x402 server (FastMCP, read-only)
- `client_365rwa.py` — minimal x402 client example
- `wellknown/mcp.json`, `wellknown/x402.json` — discovery documents
- `server.json` — MCP Registry manifest
