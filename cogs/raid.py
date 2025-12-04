import disnake
from disnake.ext import commands
from utils.sheets import get_records

class Raid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="レイド検索 🏰")
    async def raid(self, inter: disnake.ApplicationCommandInteraction, keyword: str):
        data = get_records("FF14_dutyList", "Raid")
        results = [(row["名前"], row["URL"]) for row in data if keyword in row["名前"]]
        if not results:
            await inter.response.send_message("該当するレイドが見つかりませんでした。")
            return
        desc = "\n".join([f"[{name}]({url})" for name, url in results])
        embed = disnake.Embed(title="🔎 レイド検索結果", description=desc, color=disnake.Color.red())
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Raid(bot))