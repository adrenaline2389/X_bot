from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


class ConfigError(RuntimeError):
    """Raised when required runtime configuration is missing or invalid."""


@dataclass(frozen=True)
class TwitterConfig:
    api_key: str
    api_secret: str
    access_token: str
    access_secret: str


@dataclass(frozen=True)
class PriceReportConfig:
    symbols: tuple[str, ...]
    vs_currency: str


@dataclass(frozen=True)
class WhaleAlertConfig:
    threshold_btc: float
    scan_blocks: int
    cache_path: Path


def is_dry_run() -> bool:
    value = os.getenv("X_BOT_DRY_RUN", "")
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_twitter_config() -> TwitterConfig:
    values = {
        "API_KEY": os.getenv("API_KEY"),
        "API_SECRET": os.getenv("API_SECRET"),
        "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN"),
        "ACCESS_SECRET": os.getenv("ACCESS_SECRET"),
    }
    missing = [name for name, value in values.items() if not value]
    if missing:
        names = ", ".join(missing)
        raise ConfigError(f"Missing Twitter/X environment variables: {names}")

    return TwitterConfig(
        api_key=values["API_KEY"] or "",
        api_secret=values["API_SECRET"] or "",
        access_token=values["ACCESS_TOKEN"] or "",
        access_secret=values["ACCESS_SECRET"] or "",
    )


def load_price_report_config() -> PriceReportConfig:
    raw_symbols = os.getenv("PRICE_SYMBOLS", "bitcoin")
    symbols = tuple(symbol.strip().lower() for symbol in raw_symbols.split(",") if symbol.strip())
    if not symbols:
        raise ConfigError("PRICE_SYMBOLS must contain at least one CoinGecko id.")

    vs_currency = os.getenv("PRICE_VS_CURRENCY", "usd").strip().lower()
    if not vs_currency:
        raise ConfigError("PRICE_VS_CURRENCY cannot be empty.")

    return PriceReportConfig(symbols=symbols, vs_currency=vs_currency)


def load_whale_alert_config() -> WhaleAlertConfig:
    threshold_btc = _read_float("WHALE_BTC_THRESHOLD", default=1000.0)
    if threshold_btc <= 0:
        raise ConfigError("WHALE_BTC_THRESHOLD must be greater than 0.")

    scan_blocks = _read_int("WHALE_SCAN_BLOCKS", default=6)
    if scan_blocks <= 0:
        raise ConfigError("WHALE_SCAN_BLOCKS must be greater than 0.")

    cache_path = Path(os.getenv("WHALE_CACHE_PATH", ".cache/posted_whale_txs.json"))
    return WhaleAlertConfig(
        threshold_btc=threshold_btc,
        scan_blocks=scan_blocks,
        cache_path=cache_path,
    )


def _read_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise ConfigError(f"{name} must be a number.") from exc


def _read_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer.") from exc
