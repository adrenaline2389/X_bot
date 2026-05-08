from __future__ import annotations

from datetime import datetime, timezone

from x_bot.config import PriceReportConfig, load_price_report_config
from x_bot.services.coingecko import get_simple_prices
from x_bot.twitter_client import post_tweet


SYMBOL_LABELS = {
    "bitcoin": ("Bitcoin", "BTC", "🟠"),
    "ethereum": ("Ethereum", "ETH", "🟣"),
    "solana": ("Solana", "SOL", "🟢"),
    "binancecoin": ("BNB", "BNB", "🟡"),
}


def run(config: PriceReportConfig | None = None) -> None:
    config = config or load_price_report_config()
    prices = get_simple_prices(config.symbols, config.vs_currency)
    tweet = build_price_tweet(config, prices)
    post_tweet(tweet)


def build_price_tweet(
    config: PriceReportConfig,
    prices: dict[str, dict[str, float]],
) -> str:
    currency = config.vs_currency
    lines = ["📊 Crypto Market Update"]

    for symbol in config.symbols:
        name, ticker, marker = SYMBOL_LABELS.get(symbol, (symbol.title(), symbol.upper(), "•"))
        price = prices[symbol][currency]
        lines.append(f"{marker} {name} (${ticker}): ${_format_price(price)}")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"⏰ {now}")

    tags = " ".join(f"#{SYMBOL_LABELS.get(symbol, (symbol, symbol, ''))[1]}" for symbol in config.symbols)
    lines.append(f"#Crypto {tags}".strip())
    return "\n".join(lines)


def _format_price(price: float) -> str:
    if price >= 1:
        return f"{price:,.2f}"
    return f"{price:.6f}".rstrip("0").rstrip(".")
