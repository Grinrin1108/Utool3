from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("🏓 pong!")

async def setup(bot):
    # ここで二重登録していないか注意！
    await bot.add_cog(Ping(bot))
