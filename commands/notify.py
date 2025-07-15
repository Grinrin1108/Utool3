from discord import app_commands
from discord.ext import commands
from discord import Interaction, Embed
from models.notification import Session, Notification

class Notify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify")
    async def notify_group(self, interaction: Interaction):
        await interaction.response.send_message("サブコマンドを使ってね～", ephemeral=True)

    @app_commands.command(name="configure", description="通知設定")
    async def configure(self, interaction: Interaction):
        voice = interaction.user.voice
        if not voice or not voice.channel:
            await interaction.response.send_message("ボイスチャンネルに入ってから実行してね。", ephemeral=True)
            return

        session = Session()
        notif = Notification(
            guild_id=str(interaction.guild_id),
            voice_channel_id=str(voice.channel.id),
            text_channel_id=str(interaction.channel_id)
        )
        session.merge(notif)
        session.commit()
        session.close()

        await interaction.response.send_message(f"{voice.channel.name} への入室通知をこのチャンネルに設定したよ～")

    @app_commands.command(name="delete", description="通知設定削除")
    async def delete(self, interaction: Interaction):
        session = Session()
        session.query(Notification).filter_by(
            guild_id=str(interaction.guild_id),
            text_channel_id=str(interaction.channel_id)
        ).delete()
        session.commit()
        session.close()
        await interaction.response.send_message("通知設定を削除したよ～")

    @app_commands.command(name="status", description="このチャンネルの通知設定確認")
    async def status(self, interaction: Interaction):
        session = Session()
        notifs = session.query(Notification).filter_by(
            guild_id=str(interaction.guild_id),
            text_channel_id=str(interaction.channel_id)
        ).all()
        session.close()

        if not notifs:
            await interaction.response.send_message("通知設定はありません。")
            return

        channels = "\n".join([f"<#{n.voice_channel_id}>" for n in notifs])
        embed = Embed(title="通知設定中のボイスチャンネル", description=channels)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Notify(bot))
