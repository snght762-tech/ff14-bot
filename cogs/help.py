import disnake
from disnake.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Botコマンド一覧 📖")
    async def hp(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="📖 Botコマンド一覧", description="このBotで使えるコマンドだよ！", color=disnake.Color.blue())
        embed.add_field(name="/omikuji", value="今日の運勢を占います 🔮", inline=False)
        embed.add_field(name="/images YYYYMMDD", value="指定日付に近い画像を取得 🖼", inline=False)
        embed.add_field(name="/ids キーワード", value="FF14 ID検索 ⚔️", inline=False)
        embed.add_field(name="/alliance キーワード", value="アライアンス検索 🛡️", inline=False)
        embed.add_field(name="/raid キーワード", value="レイド検索 🏰", inline=False)
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))