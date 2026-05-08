from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from x_bot.config import WhaleAlertConfig, load_whale_alert_config
from x_bot.services.blockchain import get_block_transactions, get_latest_block_height, satoshi_to_btc
from x_bot.twitter_client import post_tweet


@dataclass(frozen=True)
class WhaleTransaction:
    block_height: int
    tx_hash: str
    amount_btc: float


def run(config: WhaleAlertConfig | None = None) -> None:
    config = config or load_whale_alert_config()
    seen_hashes = _load_seen_hashes(config.cache_path)
    alerts = find_whale_transactions(config, seen_hashes)

    if not alerts:
        print("No new BTC whale transactions found.")
        _save_seen_hashes(config.cache_path, seen_hashes)
        return

    posted_hashes: set[str] = set()
    for alert in alerts:
        posted = post_tweet(build_whale_tweet(alert))
        if posted:
            posted_hashes.add(alert.tx_hash)

    if posted_hashes:
        seen_hashes.update(posted_hashes)
    _save_seen_hashes(config.cache_path, seen_hashes)


def find_whale_transactions(
    config: WhaleAlertConfig,
    seen_hashes: set[str],
) -> list[WhaleTransaction]:
    latest_height = get_latest_block_height()
    first_height = max(0, latest_height - config.scan_blocks + 1)
    alerts: list[WhaleTransaction] = []

    for block_height in range(first_height, latest_height + 1):
        for tx in get_block_transactions(block_height):
            tx_hash = tx.get("hash")
            if not tx_hash or tx_hash in seen_hashes:
                continue

            total_satoshi = sum(int(output.get("value", 0)) for output in tx.get("out", []))
            amount_btc = satoshi_to_btc(total_satoshi)
            if amount_btc >= config.threshold_btc:
                alerts.append(
                    WhaleTransaction(
                        block_height=block_height,
                        tx_hash=tx_hash,
                        amount_btc=amount_btc,
                    )
                )

    return alerts


def build_whale_tweet(alert: WhaleTransaction) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return "\n".join(
        [
            "🐋 BTC Whale Alert",
            f"💰 {alert.amount_btc:,.2f} BTC moved in one transaction",
            f"🧱 Block: {alert.block_height}",
            f"🔗 https://www.blockchain.com/btc/tx/{alert.tx_hash}",
            f"⏰ {now}",
            "#Bitcoin #Whale",
        ]
    )


def _load_seen_hashes(path: Path) -> set[str]:
    if not path.exists():
        return set()

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    hashes = data.get("posted_tx_hashes", [])
    if not isinstance(hashes, list):
        return set()
    return {item for item in hashes if isinstance(item, str)}


def _save_seen_hashes(path: Path, seen_hashes: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "posted_tx_hashes": sorted(seen_hashes)[-5000:],
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
