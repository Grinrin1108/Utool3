import os
from dotenv import load_dotenv
import discord
from flask import Flask, request
from threading import Thread

# ====== 環境変数読み込み ======
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ====== Discord Bot の設定 ======
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

# ====== Flask サーバー設定 ======
app = Flask(__name__)
post_count = 0  # POST 回数カウント用のグローバル変数

@app.route("/", methods=["GET"])
def home():
    return '<a href="https://note.com/exteoi/n/n0ea64e258797">解説はこちら</a> にあります。'

@app.route("/", methods=["POST"])
def webhook():
    global post_count
    print("📩 Received POST request.")
    post_count += 1

    if post_count == 10:
        trigger()
        post_count = 0

    return "POST response by Railway"

def trigger():
    print("🔔 Trigger called! (10 POSTs received)")

def run_flask():
    app.run(host="0.0.0.0", port=3000)

def keep_alive():
    thread = Thread(target=run_flask)
    thread.start()

# ====== 実行 ======
if __name__ == "__main__":
    keep_alive()         # Flask サーバー起動
    client.run(TOKEN)    # Discord Bot 起動
