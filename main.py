import os
import discord
from discord.ext import commands
from flask import Flask, request
from threading import Thread

# 環境変数読み込み（.envにDISCORD_TOKEN）
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容の取得許可
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Flaskアプリの準備
app = Flask(__name__)
post_count = 0

@app.route("/", methods=["GET"])
def home():
    return '<a href="https://note.com/exteoi/n/n0ea64e258797">解説はこちら</a>'

@app.route("/", methods=["POST"])
def webhook():
    global post_count
    post_count += 1
    print(f"Received POST #{post_count}")

    if post_count == 10:
        post_count = 0
        # ここに通知チェックなどの処理を入れる
        print("🔔 10回のPOST受信でトリガー発火！")

    return "OK", 200

def run_flask():
    app.run(host="0.0.0.0", port=3000)

def keep_alive():
    thread = Thread(target=run_flask)
    thread.start()

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
