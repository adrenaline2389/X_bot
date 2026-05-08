from __future__ import annotations


def get_simple_prices(symbols: tuple[str, ...], vs_currency: str) -> dict[str, dict[str, float]]:
    import requests

    params = {
        "ids": ",".join(symbols),
        "vs_currencies": vs_currency,
    }
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    missing = [symbol for symbol in symbols if symbol not in data]
    if missing:
        names = ", ".join(missing)
        raise ValueError(f"CoinGecko response missing symbols: {names}")

    return data
