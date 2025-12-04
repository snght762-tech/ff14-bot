import disnake
from disnake.ext import commands
from utils.sheets import get_records

class IDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="FF14 ID検索 ⚔️")
    async def ids(self, inter: disnake.ApplicationCommandInteraction, keyword: str):
        data = get_records("FF14_dutyList", "ID")
        results = [(row["名前"], row["URL"]) for row in data if keyword in row["名前"]]

        if not results:
            await inter.response.send_message("該当するIDが見つかりませんでした。")
            return

        desc = "\n".join([f"[{name}]({url})" for name, url in results])
        embed = disnake.Embed(
            title=f"🔎 ID検索結果（キーワード: {keyword})",
            description=desc,
            color=disnake.Color.blue()
        )
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(IDS(bot))