from unittest import TestCase

from x_bot.config import PriceReportConfig
from x_bot.features.price_report import build_price_tweet


class PriceReportTests(TestCase):
    def test_builds_default_btc_tweet(self) -> None:
        tweet = build_price_tweet(
            PriceReportConfig(symbols=("bitcoin",), vs_currency="usd"),
            {"bitcoin": {"usd": 123456.789}},
        )

        self.assertIn("Bitcoin", tweet)
        self.assertIn("$123,456.79", tweet)
        self.assertIn("#BTC", tweet)
