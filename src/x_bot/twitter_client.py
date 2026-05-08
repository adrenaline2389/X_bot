from __future__ import annotations

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
        print("[dry-run] Tweet not posted:")
        print(text)
        return False

    client = client or create_client()
    client.create_tweet(text=text)
    print("Tweet posted:")
    print(text)
    return True
