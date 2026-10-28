"""365rwa x402 真钱验证客户端：verify_rwa_project 付费调用 + Base 链上核验。

复用 rentgpu 的测试买家钱包（/opt/x402-gpu-mcp/secrets/wallets.json，不外传不打印私钥）。
用法：venv/bin/python client_365rwa.py
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

from eth_account import Account
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from web3 import Web3

from x402 import x402Client
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact import ExactEvmScheme
from x402.mcp import wrap_mcp_client_with_payment

NETWORK = os.environ.get("X402_NETWORK", "eip155:8453")
RPC = os.environ.get("BASE_RPC", "https://base-rpc.publicnode.com")
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
SERVER = os.environ.get("MCP_URL", "https://365rwa.vip/mcp")
WALLETS = Path("/opt/x402-gpu-mcp/secrets/wallets.json")
SELLER = "0x230cd9cd33589bcf33cd32e5aa4f9e0c3994a63b"

_BAL_ABI = [{
    "inputs": [{"name": "account", "type": "address"}],
    "name": "balanceOf",
    "outputs": [{"name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function",
}]


class _SessionAdapter:
    def __init__(self, session):
        self._s = session

    async def call_tool(self, params: dict, **kwargs):
        return await self._s.call_tool(
            name=params["name"],
            arguments=params.get("arguments") or {},
            meta=params.get("_meta"),
            **kwargs,
        )

    def __getattr__(self, name):
        return getattr(self._s, name)


def usdc_balance(addr: str) -> float:
    w3 = Web3(Web3.HTTPProvider(RPC))
    c = w3.eth.contract(address=Web3.to_checksum_address(USDC), abi=_BAL_ABI)
    return c.functions.balanceOf(Web3.to_checksum_address(addr)).call() / 10**6


def transfers_between(from_addr: str, to_addr: str, blocks: int = 600) -> list[dict]:
    w3 = Web3(Web3.HTTPProvider(RPC))
    topic = w3.keccak(text="Transfer(address,address,uint256)").hex()
    pad = lambda a: "0x" + "0" * 24 + a[2:].lower()
    latest = w3.eth.block_number
    logs = w3.eth.get_logs({
        "fromBlock": latest - blocks, "toBlock": "latest",
        "address": Web3.to_checksum_address(USDC),
        "topics": [topic, pad(from_addr), pad(to_addr)],
    })
    return [{"block": l["blockNumber"], "tx": l["transactionHash"].hex(),
             "amount": int(l["data"].hex(), 16) / 10**6} for l in logs]


def _fmt(res) -> str:
    return "\n".join(t for c in getattr(res, "content", []) or [] if (t := getattr(c, "text", None)))


async def main() -> int:
    w = json.loads(WALLETS.read_text(encoding="utf-8"))
    buyer_key, buyer_addr = w["buyer"]["key"], w["buyer"]["address"]

    print("=" * 68)
    print("x402 真钱验证 · 365rwa RWA 数据 MCP")
    print("=" * 68)
    print(f"买方: {buyer_addr}")
    print(f"卖方: {SELLER}")
    print(f"端点: {SERVER}")

    bal_before = usdc_balance(buyer_addr)
    seller_before = usdc_balance(SELLER)
    print(f"付款前余额: buyer {bal_before:.6f} | seller {seller_before:.6f} USDC")
    if bal_before < 0.05:
        print("[!] 买家 USDC 不足 $0.05，无法验证")
        return 2

    account = Account.from_key(buyer_key)
    signer = EthAccountSigner(account)
    x402_client = x402Client()
    x402_client.register(NETWORK, ExactEvmScheme(signer))

    async with streamable_http_client(SERVER) as (r, w_stream, _):
        async with ClientSession(r, w_stream) as session:
            await session.initialize()
            mcp = wrap_mcp_client_with_payment(
                _SessionAdapter(session), x402_client,
                auto_payment=True, on_payment_requested=lambda ctx: True,
            )
            print("\n--- 付费调用 verify_rwa_project(name='BUIDL') $0.05 ---")
            res = await mcp.call_tool("verify_rwa_project", {"name": "BUIDL"})
            print(f"isError = {getattr(res, 'isError', None)}")
            body = _fmt(res)
            try:
                parsed = json.loads(body)
                print(json.dumps({k: parsed[k] for k in ('query', 'verdict', 'verdict_zh', 'hits') if k in parsed},
                                 ensure_ascii=False))
            except Exception:
                print(body[:400])

    print("\n等待链上确认…")
    await asyncio.sleep(8)
    txs = transfers_between(buyer_addr, SELLER)
    total = sum(t["amount"] for t in txs)
    print(f"\n链上核验：buyer → seller 转账 {len(txs)} 笔，合计 {total:.6f} USDC")
    for t in txs:
        print(f"  {t['amount']:.6f} USDC  blk {t['block']}  https://basescan.org/tx/{t['tx']}")
    print(f"余额变化: buyer {bal_before:.6f} → {usdc_balance(buyer_addr):.6f} | "
          f"seller {seller_before:.6f} → {usdc_balance(SELLER):.6f}")
    ok = len(txs) >= 1 and total >= 0.05
    print("\n结论:", "✅ 真钱链路跑通 — 付费 → 结算 → 卖方到账" if ok else "❌ 链上未查到转账")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
