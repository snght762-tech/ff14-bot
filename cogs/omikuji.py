import disnake
from disnake.ext import commands
import random
from datetime import datetime, timezone, timedelta

class Omikuji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.JST = timezone(timedelta(hours=9))
    
    # Help用の情報を持たせる
    help_info = {
        "command": "/omikuji",
        "description": "今日の運勢を占います 🔮"
    }

    @commands.slash_command(description="今日の運勢を占います 🔮")
    async def omikuji(self, inter: disnake.ApplicationCommandInteraction):
        JST = timezone(timedelta(hours=9))
        today_str = datetime.now(JST).strftime("%Y-%m-%d")
        user_id = inter.author.id
        seed_str = f"{today_str}:{user_id}"
        rng = random.Random(seed_str)

        # 総合評価
        luck_levels = ["大吉", "中吉", "小吉", "吉", "末吉", "凶"]
        luck_emojis = {"大吉":"🎉", "中吉":"😊", "小吉":"🙂", "吉":"🍀", "末吉":"😐", "凶":"💀"}
        luck = rng.choice(luck_levels)
        luck_emoji = luck_emojis[luck]

        # カテゴリ別運勢（7カテゴリ）
        categories = ["恋愛運", "金運", "仕事・学業運", "健康運", "味方運", "ロット運", "ガチャ運"]
        scores = [rng.randint(0, 5) for _ in categories]
        stars = [f"{'★'*s}{'☆'*(5-s)} ({s}/5)" for s in scores]
        avg_score = sum(scores) / len(scores)

        # ラッキーアイテム
        items = ["ラーメン 🍜", "マウント 🐉", "ミニオン 🐾", "エモート 💃", "ギル 💰", "チョコボ 🐤"]
        lucky_item = rng.choice(items)

        # Embed生成
        embed = disnake.Embed(
            title="🔮 今日の御籤（おみくじ）",
            description=f"{inter.author.display_name} の運勢だよ！ ({today_str} JST)",
            color=disnake.Color.purple()
        )
        embed.add_field(name="総合評価", value=f"{luck} {luck_emoji}", inline=False)

        for cat, star in zip(categories, stars):
            embed.add_field(name=cat, value=star, inline=True)

        embed.add_field(name="ラッキーアイテム", value=lucky_item, inline=False)
        embed.add_field(name="平均スコア", value=f"{avg_score:.1f} / 5.0", inline=False)
        embed.set_footer(text="※同じ日は同じ結果になります（翌日更新）")

        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Omikuji(bot))
