from discord import app_commands
from discord.ext import commands
import sqlite3

class YoutubeNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_db()

    def init_db(self):
        self.conn = sqlite3.connect("database.db")
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS notifications (
            guild_id TEXT,
            text_channel_id TEXT,
            youtube_channel_id TEXT
        )''')
        self.conn.commit()

    @app_commands.command(name="youtube_add", description="YouTube通知を追加するよ～")
    @app_commands.describe(channel_id="YouTubeのチャンネルID")
    async def add_notify(self, interaction, channel_id: str):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO notifications VALUES (?, ?, ?)", (
            str(interaction.guild_id),
            str(interaction.channel_id),
            channel_id
        ))
        self.conn.commit()
        await interaction.response.send_message(f"✅ 通知追加完了: `{channel_id}`")

    @app_commands.command(name="youtube_remove", description="通知を削除するよ～")
    @app_commands.describe(channel_id="YouTubeのチャンネルID")
    async def remove_notify(self, interaction, channel_id: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM notifications WHERE guild_id=? AND text_channel_id=? AND youtube_channel_id=?", (
            str(interaction.guild_id),
            str(interaction.channel_id),
            channel_id
        ))
        self.conn.commit()
        await interaction.response.send_message(f"🗑️ 削除完了: `{channel_id}`")

async def setup(bot):
    await bot.add_cog(YoutubeNotify(bot))
