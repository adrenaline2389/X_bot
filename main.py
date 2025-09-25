import requests
import tweepy
import os
from datetime import datetime

# ====== Twitter API Key ======
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# ====== 获取多个价格 ======
def get_prices(symbols):
    ids = ",".join(symbols)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    r = requests.get(url, timeout=10)
    return r.json()

# ====== 一条推包含4个标的价格 ======
def tweet_prices():
    symbols = ["bitcoin", "ethereum", "solana", "binancecoin"]
    names = {
        "bitcoin": ("Bitcoin", "BTC", "🟠"),
        "ethereum": ("Ethereum", "ETH", "🟣"),
        "solana": ("Solana", "SOL", "🟢"),
        "binancecoin": ("BNB", "BNB", "🟡"),
    }

    data = get_prices(symbols)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = ["📊 Market Price Update"]
    for s in symbols:
        name, ticker, emoji = names[s]
        price = data[s]["usd"]
        lines.append(f"{emoji} {name} (${ticker}): ${price}")

    lines.append(f"⏰ {now}")
    lines.append("#Crypto #BTC #ETH #SOL #BNB")

    text = "\n".join(lines)
    client.create_tweet(text=text)
    print("✅ 价格播报成功:", text)


# ====== 鲸鱼转账提醒 ======
def get_latest_block_height():
    url = "https://blockchain.info/q/getblockcount"
    r = requests.get(url, timeout=10)
    return int(r.text)

def get_block_transactions(block_height):
    url = f"https://blockchain.info/block-height/{block_height}?format=json"
    r = requests.get(url, timeout=10)
    data = r.json()
    return data["blocks"][0]["tx"]

def satoshi_to_btc(satoshi):
    return satoshi / 100_000_000

def tweet_whale_alert(amount, tx_hash):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = (
        f"🐋 Whale Alert\n"
        f"💰 {amount:.2f} BTC transferred\n"
        f"🔗 https://www.blockchain.com/btc/tx/{tx_hash}\n"
        f"⏰ {now}\n"
        f"#Bitcoin #Whale"
    )
    client.create_tweet(text=text)
    print("✅ 鲸鱼提醒成功:", text)

def check_whale_transactions():
    try:
        latest_height = get_latest_block_height()
        txs = get_block_transactions(latest_height)
        for tx in txs:
            total_out = sum(out["value"] for out in tx["out"])
            amount_btc = satoshi_to_btc(total_out)
            if amount_btc >= 5000:
                tweet_whale_alert(amount_btc, tx["hash"])
    except Exception as e:
        print("❌ 鲸鱼检测失败:", e)
