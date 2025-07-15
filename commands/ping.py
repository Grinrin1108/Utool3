# commands/ping.py
import discord
from discord import app_commands

class PingCommand:
    def __init__(self, tree):
        @tree.command(name="ping", description="Pingを返します")
        async def ping(interaction: discord.Interaction):
            await interaction.response.send_message("Pong!", ephemeral=True)
