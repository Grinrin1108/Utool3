import discord
from discord.ext import commands
from discord import app_commands

NERF_ROLE_ID = 1303270351429697586  # Nerfロール ID
ADMIN_ROLE_ID = 1356850745634324651  # 管理者ロール ID

class Unnerf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unnerf", description="全ステータス大ダウン解除コマンド")
    @app_commands.describe(user="全ステータス大ダウン解除するユーザー")
    async def unnerf(self, interaction: discord.Interaction, user: discord.Member):
        # 管理者ロールチェック
        if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("権限がないみたい…", ephemeral=True)
            return

        # Nerfロールを取得して解除
        nerf_role = interaction.guild.get_role(NERF_ROLE_ID)
        if nerf_role:
            await user.remove_roles(nerf_role)
            await interaction.response.send_message(f"{user.mention} を全ステータス大ダウン解除しました。")
        else:
            await interaction.response.send_message("Nerfロールが見つかりませんでした。")

async def setup(bot):
    await bot.add_cog(Unnerf(bot))
