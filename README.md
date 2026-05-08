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
