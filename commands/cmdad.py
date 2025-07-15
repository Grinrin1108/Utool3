import discord
from discord.ext import commands
from discord import app_commands

CMD_ROLE_ID = 1356850745634324651  # コマンド許可ロールのID
ADMIN_ROLE_ID = 1356850745634324651  # 管理者ロールのID（必要に応じて変更）

class CmdAd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cmdad", description="コマンド権限を付与します")
    @app_commands.describe(user="コマンドを許可するユーザー")
    async def cmdad(self, interaction: discord.Interaction, user: discord.Member):
        # 呼び出し元が admin ロールを持っているかチェック
        if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("権限がないみたい…", ephemeral=True)
            return

        role = interaction.guild.get_role(CMD_ROLE_ID)
        if role:
            await user.add_roles(role)
            await interaction.response.send_message(f"{user.mention} にコマンドを許可しました。")
        else:
            await interaction.response.send_message("コマンド権限ロールが見つかりませんでした。")

async def setup(bot):
    await bot.add_cog(CmdAd(bot))
