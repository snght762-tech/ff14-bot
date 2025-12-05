import disnake
from disnake.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Botコマンド一覧 📖")
    async def hp(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="📖 Botコマンド一覧",
            description="このBotで使えるコマンドだよ！",
            color=disnake.Color.blue()
        )

        # 全Cogを走査して help_info があれば追加
        for cog in self.bot.cogs.values():
            if hasattr(cog, "help_info"):
                info = cog.help_info
                embed.add_field(name=info["command"], value=info["description"], inline=False)

        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))