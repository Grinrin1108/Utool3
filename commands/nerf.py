import discord
from discord.ext import commands
from discord import app_commands

NERF_ROLE_ID = 1303270351429697586  # 全ステータス大ダウンロール ID
ADMIN_ROLE_ID = 1356850745634324651  # 管理者ロール ID

class Nerf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="nerf", description="全ステータス大ダウンコマンド")
    @app_commands.describe(user="全ステータス大ダウンにするユーザー")
    async def nerf(self, interaction: discord.Interaction, user: discord.Member):
        # 管理者ロールの所持チェック
        if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("権限がないみたい…", ephemeral=True)
            return

        # Nerf ロールを取得して追加
        nerf_role = interaction.guild.get_role(NERF_ROLE_ID)
        if nerf_role:
            await user.add_roles(nerf_role)
            await interaction.response.send_message(f"{user.mention} を全ステータス大ダウンしました。")
        else:
            await interaction.response.send_message("全ステータス大ダウンロールが見つかりませんでした。")

async def setup(bot):
    await bot.add_cog(Nerf(bot))
