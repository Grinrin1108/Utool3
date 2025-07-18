import os
import glob
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from threading import Thread
import discord
from discord.ext import commands
from youtube import get_latest_video  # ← 追加

# ====== 環境変数読み込み ======
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ====== Discord Bot の設定 ======
intents = discord.Intents.all()
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
    await bot.process_commands(message)

# ====== コマンドハンドラ読み込み ======
async def load_commands():
    for filepath in glob.glob("commands/*.py"):
        name = os.path.splitext(os.path.basename(filepath))[0]
        print(f"🔄 Loading command: {name}")
        await bot.load_extension(f"commands.{name}")

# ====== トリガー処理 ======
async def trigger():
    print("🔔 Trigger called! (10 POSTs received)")

    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
    video = get_latest_video(channel_id)

    if video:
        print("📹 最新動画:")
        print("タイトル:", video['title'])
        print("URL:", video['link'])
    else:
        print("❌ 動画が取得できませんでした。")

# ====== 実行 ======
if __name__ == "__main__":
    keep_alive()

    async def start_bot():
        await load_commands()
        await bot.start(TOKEN)

    asyncio.run(start_bot())
