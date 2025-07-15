import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from flask import Flask, request
from threading import Thread

# ====== 環境変数読み込み ======
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ====== Discord Bot の設定 ======
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得可能に
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print(f"[送信] {message.author}: {message.content}")
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if before.content == after.content:
        return
    print(f"[編集] {before.author}\n旧: {before.content}\n新: {after.content}")

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    print(f"[削除] {message.author}: {message.content}")

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
    bot.run(TOKEN)       # Discord Bot 起動
