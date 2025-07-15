import os
from dotenv import load_dotenv
import discord

load_dotenv()
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
