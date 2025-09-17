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

# ====== 获取 BTC 价格并发推 ======
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    r = requests.get(url, timeout=10)
    return r.json()["bitcoin"]["usd"]

def tweet_btc_price():
    price = get_btc_price()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"🟠 Bitcoin Price Update\n💰 ${price}\n⏰ {now}\n#Bitcoin #BTC"
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
