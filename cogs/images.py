import disnake
from disnake.ext import commands
from datetime import datetime, timezone

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Help用の情報を持たせる
    help_info = {
        "command": "/images",
        "description": "指定した日付に近い画像を3件取得します。現在オプション作成中"
    }

    @commands.slash_command(description="指定日付に近い画像を取得 🖼")
    async def images(self, inter: disnake.ApplicationCommandInteraction, date_str: str):
        try:
            target_date = datetime.strptime(date_str, "%Y%m%d").replace(tzinfo=timezone.utc)
        except ValueError:
            await inter.response.send_message("日付は YYYYMMDD 形式で指定してください。", ephemeral=True)
            return
        await inter.response.send_message(f"検索対象日: {target_date.strftime('%Y-%m-%d')}")
        
def setup(bot):
    bot.add_cog(Images(bot))