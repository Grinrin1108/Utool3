import os
import glob
from dotenv import load_dotenv
from flask import Flask, request
from threading import Thread
import discord
from discord.ext import commands
import asyncio

# ====== 環境変数読み込み ======
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ====== Discord Bot の設定 ======
intents = discord.Intents.all()  # 特権インテントを含む
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ====== Flask サーバー設定 ======
app = Flask(__name__)
post_count = 0

@app.route("/", methods=["GET"])
def home():
    return '<a href="https://note.com/exteoi/n/n0ea64e258797">解説はこちら</a> にあります。'

@app.route("/", methods=["POST"])
def webhook():
    global post_count
    print("📩 Received POST request.")
    post_count += 1

    if post_count == 10:
        asyncio.run(trigger())
        post_count = 0

    return "POST response by Railway"

def run_flask():
    app.run(host="0.0.0.0", port=3000)

def keep_alive():
    thread = Thread(target=run_flask)
    thread.start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)  # ← これを忘れるとコマンドが2回実行されることがある

# ====== コマンドハンドラ読み込み ======
async def load_commands():
    for filepath in glob.glob("commands/*.py"):
        name = os.path.splitext(os.path.basename(filepath))[0]
        print(f"🔄 Loading command: {name}")  # ← ログ出力を追加
        await bot.load_extension(f"commands.{name}")

# ====== トリガー処理（仮） ======
async def trigger():
    print("🔔 Trigger called! (10 POSTs received)")
    # 本来はYouTube通知などの処理がここに入る予定

# ====== 実行 ======
if __name__ == "__main__":
    keep_alive()

    async def start_bot():
        await load_commands()
        await bot.start(TOKEN)

    asyncio.run(start_bot())
