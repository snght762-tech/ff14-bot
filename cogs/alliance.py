import disnake
from disnake.ext import commands
from utils.sheets import get_records

class Alliance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="アライアンス検索 🛡️")
    async def alliance(self, inter: disnake.ApplicationCommandInteraction, keyword: str):
        data = get_records("FF14_dutyList", "Alliance")
        results = [(row["名前"], row["URL"]) for row in data if keyword in row["名前"]]
        if not results:
            await inter.response.send_message("該当するアライアンスが見つかりませんでした。")
            return
        desc = "\n".join([f"[{name}]({url})" for name, url in results])
        embed = disnake.Embed(title="🔎 アライアンス検索結果", description=desc, color=disnake.Color.green())
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Alliance(bot))
