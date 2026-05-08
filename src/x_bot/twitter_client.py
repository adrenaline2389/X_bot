from __future__ import annotations

import sys
from typing import Any

from x_bot.config import TwitterConfig, is_dry_run, load_twitter_config


def create_client(config: TwitterConfig | None = None) -> Any:
    import tweepy

    config = config or load_twitter_config()
    return tweepy.Client(
        consumer_key=config.api_key,
        consumer_secret=config.api_secret,
        access_token=config.access_token,
        access_token_secret=config.access_secret,
    )


def post_tweet(text: str, client: Any | None = None) -> bool:
    if is_dry_run():
        _print_line("[dry-run] Tweet not posted:")
        _print_line(text)
        return False

    client = client or create_client()
    client.create_tweet(text=text)
    _print_line("Tweet posted:")
    _print_line(text)
    return True


def _print_line(text: str) -> None:
    _prefer_utf8_stdout()
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        safe_text = text.encode(encoding, errors="backslashreplace").decode(encoding)
        print(safe_text)


def _prefer_utf8_stdout() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is None:
        return

    try:
        reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        return
