from __future__ import annotations


SATOSHIS_PER_BTC = 100_000_000


def get_latest_block_height() -> int:
    import requests

    response = requests.get("https://blockchain.info/q/getblockcount", timeout=10)
    response.raise_for_status()
    return int(response.text)


def get_block_transactions(block_height: int) -> list[dict]:
    import requests

    response = requests.get(
        f"https://blockchain.info/block-height/{block_height}",
        params={"format": "json"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    blocks = data.get("blocks", [])
    if not blocks:
        raise ValueError(f"No block data returned for height {block_height}.")
    return blocks[0].get("tx", [])


def satoshi_to_btc(satoshi: int) -> float:
    return satoshi / SATOSHIS_PER_BTC
