from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("🏓 pong!")

async def setup(bot):  # ← 非同期に変更
    await bot.add_cog(Ping(bot))  # ← await を追加
