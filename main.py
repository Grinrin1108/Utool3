import os
from dotenv import load_dotenv
from flask import Flask, request
from threading import Thread
import discord
from discord.ext import commands

# ==== 環境変数 ====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ==== Discord Bot セットアップ ====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# ==== Flask (Webhook受信用) ====
app = Flask(__name__)
post_count = 0

@app.route("/", methods=["GET"])
def index():
    return "✅ Railway Python Bot is working!"

@app.route("/", methods=["POST"])
def webhook():
    global post_count
    post_count += 1
    print(f"📩 POST received ({post_count}/10)")
    
    if post_count == 10:
        print("🔔 Trigger! 10 POSTs received.")
        post_count = 0
    
    return "OK", 200

def run_flask():
    app.run(host="0.0.0.0", port=3000)

def keep_alive():
    thread = Thread(target=run_flask)
    thread.start()

# ==== 実行 ====
if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
