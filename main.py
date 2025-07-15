import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask, request
from threading import Thread
import importlib.util
import glob

# Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Flask setup
app = Flask(__name__)
post_count = 0

@app.route("/", methods=["POST"])
def webhook():
    global post_count
    post_count += 1
    print("📩 POST received")
    if post_count >= 10:
        bot.loop.create_task(trigger())
        post_count = 0
    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "🚀 Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=3000)

def keep_alive():
    Thread(target=run_flask).start()

# Trigger example
async def trigger():
    print("🔔 Triggered after 10 POSTs")

# Load commands
def load_commands():
    for filepath in glob.glob("commands/*.py"):
        name = os.path.splitext(os.path.basename(filepath))[0]
        bot.load_extension(f"commands.{name}")

# Events
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    from handlers.message_create import handle_message
    await handle_message(message)
    await bot.process_commands(message)

if __name__ == "__main__":
    keep_alive()
    load_commands()
    bot.run(TOKEN)
