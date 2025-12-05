import disnake
from disnake.ext import commands

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1h6mVVDFOy2LzBguuFzoWDHF_JVqucO2ghluEBiC0jA4/edit?gid=0#gid=0"

class RaidSheet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Help用の情報を持たせる
    help_info = {
        "command": "/raidlist",
        "description": "各種情報管理スプレッドシートのリンクを表示します"
    }

    @commands.slash_command(
            description="情報管理スプレッドシートのリンクを返す 📑",
            guild_ids=[1325451193115345059]
    )
    async def raidlist(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="📑 レイド・ID管理スプレッドシート",
            description=f"[こちらをクリックして開く]({SPREADSHEET_URL})",
            color=disnake.Color.green()
        )
        embed.set_footer(text="Googleスプレッドシートで管理中")
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(RaidSheet(bot))
