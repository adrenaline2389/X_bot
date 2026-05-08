from unittest import TestCase

from x_bot.features.whale_alert import WhaleTransaction, build_whale_tweet


class WhaleAlertTests(TestCase):
    def test_builds_btc_whale_tweet(self) -> None:
        tweet = build_whale_tweet(
            WhaleTransaction(
                block_height=900000,
                tx_hash="abc123",
                amount_btc=1000.5,
            )
        )

        self.assertIn("BTC Whale Alert", tweet)
        self.assertIn("1,000.50 BTC", tweet)
        self.assertIn("https://www.blockchain.com/btc/tx/abc123", tweet)
