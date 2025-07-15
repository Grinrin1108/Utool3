import discord
from discord.ext import commands
from discord import app_commands

MUTE_ROLE_ID = 1288263740680306750  # ミュートロール ID
ADMIN_ROLE_ID = 1356850745634324651  # 管理者ロール ID

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unmute", description="ミュート解除コマンド")
    @app_commands.describe(user="ミュート解除するユーザー")
    async def unmute(self, interaction: discord.Interaction, user: discord.Member):
        # 管理者ロールの所持チェック
        if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("権限がないみたい…", ephemeral=True)
            return

        # ミュートロールを取得して解除
        mute_role = interaction.guild.get_role(MUTE_ROLE_ID)
        if mute_role:
            await user.remove_roles(mute_role)
            await interaction.response.send_message(f"{user.mention} をミュート解除しました。")
        else:
            await interaction.response.send_message("ミュートロールが見つかりませんでした。")

async def setup(bot):
    await bot.add_cog(Unmute(bot))
