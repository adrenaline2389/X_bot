# X Bot

X Bot is a GitHub Actions driven Twitter/X bot for crypto updates.

Current features:

- Price report: posts configured crypto market prices, defaulting to BTC/USD.
- BTC whale alert: scans recent Bitcoin blocks and posts transactions above a configurable BTC threshold.

## Project Structure

```text
src/x_bot/
  main.py                 # command dispatcher
  config.py               # environment variable parsing
  twitter_client.py       # Twitter/X posting
  features/
    price_report.py       # market price tweet
    whale_alert.py        # BTC whale alert tweet
  services/
    coingecko.py          # CoinGecko HTTP client
    blockchain.py         # blockchain.info HTTP client
```

GitHub Actions workflows:

- `.github/workflows/price-report.yml`: runs every 4 hours.
- `.github/workflows/whale-alert.yml`: runs every 15 minutes.

## GitHub Secrets

Set these repository secrets before enabling the workflows:

```text
API_KEY
API_SECRET
ACCESS_TOKEN
ACCESS_SECRET
```

For posting, the X Developer app must have `Read and write` permissions. If you change
the app permission, regenerate `ACCESS_TOKEN` and `ACCESS_SECRET` after the permission
change, then update the GitHub repository secrets.

## X API Cost Notice

This bot posts through the official X API. X API access is paid usage: the account
owner must purchase or enable API credits in the X Developer Console before the
workflows can create posts.

Typical posting costs:

```text
Price report post: plain text post, charged as Content: Create.
Whale alert post: includes a blockchain.com URL, which may be charged as Content: Create with URL.
```

If the app permissions and secrets are correct but posting fails with `403 Forbidden`,
check the X Developer Console billing, credits, API access, and account status.

Optional repository variables:

```text
PRICE_SYMBOLS=bitcoin
PRICE_VS_CURRENCY=usd
WHALE_BTC_THRESHOLD=1000
WHALE_SCAN_BLOCKS=6
```

`PRICE_SYMBOLS` accepts CoinGecko ids separated by commas, for example:

```text
bitcoin,ethereum,solana,binancecoin
```

## Local Test

```powershell
python -m pip install -r requirements.txt
$env:X_BOT_DRY_RUN="true"
python -m x_bot price-report
python -m x_bot whale-alert
```

Dry run mode prints tweet text but does not post to Twitter/X.
