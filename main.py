import os
import tweepy
import requests
import schedule
import time
from datetime import datetime

# ====== 读取环境变量，填入 Twitter API Key ======
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# ====== 初始化 Twitter v2 Client ======
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# ====== 获取比特币价格 ======
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        print("获取价格失败:", e)
        return None

# ====== 发推文函数 ======
def tweet_btc_price():
    price = get_btc_price()
    if price:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"🟠 Bitcoin (BTC) Price Update\n💰 ${price}\n⏰ {now}\n#Bitcoin #BTC"
        try:
            response = client.create_tweet(text=message)
            print("✅ 推文发送成功:", response.data)
        except Exception as e:
            print("❌ 发推失败:", e)

# ====== 定时任务（每4小时发一次） ======
schedule.every(4).hours.do(tweet_btc_price)

print("🚀 BTC 价格播报机器人已启动...")

# 👉 先手动发一条，确认能用
tweet_btc_price()

# ====== 主循环 ======
while True:
    schedule.run_pending()
    time.sleep(10)
