import disnake
from disnake.ext import commands, tasks
import random
from datetime import datetime, timezone, timedelta
from disnake.utils import get
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# .envファイルを読み込む
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

JST = timezone(timedelta(hours=9))

# ---------- おみくじコマンド ----------
@bot.command()
async def omikuji(ctx):
    today_str = datetime.now(JST).strftime("%Y-%m-%d")
    user_id = ctx.author.id
    seed_str = f"{today_str}:{user_id}"
    rng = random.Random(seed_str)

    categories = {
        "恋愛運": rng.randint(0, 5),
        "金運": rng.randint(0, 5),
        "仕事・学業運": rng.randint(0, 5),
        "健康運": rng.randint(0, 5),
        "味方運": rng.randint(0, 5),
        "ロット運": rng.randint(0, 5),
        "ガチャ運": rng.randint(0, 5),
    }

    avg_score = sum(categories.values()) / len(categories)

    if avg_score >= 4.5:
        overall, color = "大吉 🎉", disnake.Color.gold()
    elif avg_score >= 3.5:
        overall, color = "中吉 🙂", disnake.Color.green()
    elif avg_score >= 2.5:
        overall, color = "小吉 😌", disnake.Color.blue()
    elif avg_score >= 1.5:
        overall, color = "吉 🍀", disnake.Color.purple()
    elif avg_score >= 1.0:
        overall, color = "末吉 🤔", disnake.Color.orange()
    elif avg_score >= 0.5:
        overall, color = "凶 😱", disnake.Color.red()
    else:
        overall, color = "大凶 💀", disnake.Color.dark_red()

    def stars(n): return "★" * n + "☆" * (5 - n)

    lucky_items = [
        "赤いマフラー 🧣","温かいお茶 🍵","スマホ充電器 🔌","お気に入りの本 📖",
        "イヤホン 🎧","ラーメン 🍜","猫の写真 🐱","お菓子 🍫","観葉植物 🌱","コーヒー ☕"
    ]
    lucky_item = rng.choice(lucky_items)

    embed = disnake.Embed(
        title="🔮 今日の御籤（おみくじ）",
        description=f"{ctx.author.display_name} の運勢だよ！（{today_str} JST）",
        color=color
    )
    embed.add_field(name="総合評価", value=overall, inline=False)
    for k, v in categories.items():
        embed.add_field(name=k, value=f"{stars(v)} ({v}/5)", inline=True)
    embed.add_field(name="ラッキーアイテム", value=lucky_item, inline=False)
    embed.set_footer(text=f"平均スコア：{round(avg_score, 1)} / 5.0\n※同じ日は同じ結果になります（翌日更新）")

    await ctx.send(embed=embed)

# ---------- 画像取得コマンド（botチャンネル限定） ----------
@bot.command()
async def images(ctx, date_str: str):
    # 実行チャンネル制限
    if ctx.channel.name != "botチャンネル":  # ← botチャンネル名に合わせて変更
        await ctx.send("このコマンドは bot チャンネルでのみ使用できます。")
        return

    try:
        target_date = datetime.strptime(date_str, "%Y%m%d").replace(tzinfo=timezone.utc)
    except ValueError:
        await ctx.send("日付は YYYYMMDD 形式で指定してください。例: 20251204")
        return

    # サーバー内から「ssss」という名前のチャンネルを取得
    channel = get(ctx.guild.text_channels, name="ssss")
    if channel is None:
        await ctx.send("指定したチャンネル 'ssss' が見つかりませんでした。")
        return

    try:
        messages = await channel.history(limit=500).flatten()
    except disnake.Forbidden:
        await ctx.send("そのチャンネルの履歴を読む権限がありません。")
        return

    image_messages = []
    for m in messages:
        for att in m.attachments:
            if att.content_type and att.content_type.startswith("image/"):
                diff = abs((m.created_at - target_date).total_seconds())
                image_messages.append((diff, m, att))

    image_messages.sort(key=lambda x: x[0])

    if not image_messages:
        await ctx.send("指定日付に近い画像は見つかりませんでした。")
        return

    for _, m, att in image_messages[:3]:
        await ctx.send(f"{m.created_at.strftime('%Y-%m-%d %H:%M:%S')} → {att.url}")

# ---------- Google Sheets認証 ----------
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("FF14_dutyList")

# ---------- ID検索 ----------
@bot.command()
async def IDS(ctx, *, keyword: str):
    try:
        id_sheet = sheet.worksheet("ID")
        data = id_sheet.get_all_records()
        results = [(row["名前"], row["URL"]) for row in data if keyword in row["名前"]]

        if not results:
            await ctx.send("該当するIDが見つかりませんでした。")
            return

        desc = "\n".join([f"[{name}]({url})" for name, url in results])
        embed = disnake.Embed(
            title=f"🔎 ID検索結果（キーワード: {keyword}）",
            description=desc,
            color=disnake.Color.blue()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"検索中にエラーが発生しました: {e}")

# ---------- アライアンス検索 ----------
@bot.command()
async def ALLIANCE(ctx, *, keyword: str):
    try:
        alliance_sheet = sheet.worksheet("Alliance")
        data = alliance_sheet.get_all_records()
        results = [(row["名前"], row["URL"]) for row in data if keyword in row["名前"]]

        if not results:
            await ctx.send("該当するアライアンスレイドが見つかりませんでした。")
            return

        desc = "\n".join([f"[{name}]({url})" for name, url in results])
        embed = disnake.Embed(
            title=f"🔎 アライアンス検索結果（キーワード: {keyword}）",
            description=desc,
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"検索中にエラーが発生しました: {e}")

# ---------- レイド検索 ----------
@bot.command()
async def RAID(ctx, *, keyword: str):
    try:
        raid_sheet = sheet.worksheet("Raid")
        data = raid_sheet.get_all_records()
        results = [(row["名前"], row["URL"]) for row in data if keyword in row["名前"]]

        if not results:
            await ctx.send("該当するレイドが見つかりませんでした。")
            return

        desc = "\n".join([f"[{name}]({url})" for name, url in results])
        embed = disnake.Embed(
            title=f"🔎 レイド検索結果（キーワード: {keyword}）",
            description=desc,
            color=disnake.Color.red()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"検索中にエラーが発生しました: {e}")

@bot.command(name="hp")
async def hp_command(ctx):
    embed = disnake.Embed(
        title="📖 Botコマンド一覧",
        description="このBotで使えるコマンドだよ！",
        color=disnake.Color.blue()
    )

    embed.add_field(name="!omikuji", value="今日の運勢を占います 🔮", inline=False)
    embed.add_field(name="!images YYYYMMDD", value="指定日付に近い画像を取得 🖼", inline=False)
    embed.add_field(name="!IDS キーワード", value="スプレッドシートからFF14 ID検索 ⚔️", inline=False)

    embed.set_footer(text="※コマンドは毎日更新される場合があります")

    await ctx.send(embed=embed)

@tasks.loop(minutes=1)
async def daily_omikuji():
    now = datetime.now(JST)
    # 毎日9:00に実行
    if now.hour == 9 and now.minute == 0:
        channel = disnake.utils.get(bot.get_all_channels(), name="bot")  # ←送信先チャンネル名
        if channel:
            today_str = now.strftime("%Y-%m-%d")
            embed = disnake.Embed(
                title=f"🔮 今日の御籤（おみくじ） {today_str} JST",
                description="FCメンバーの運勢一覧",
                color=disnake.Color.gold()
            )

            for guild in bot.guilds:
                for member in guild.members:
                    if not member.bot:  # Botは除外
                        seed_str = f"{today_str}:{member.id}"
                        rng = random.Random(seed_str)
                        score = rng.randint(0, 5)

                        # 星表示
                        stars = "★" * score + "☆" * (5 - score)

                        embed.add_field(
                            name=member.display_name,
                            value=f"{stars} ({score}/5)",
                            inline=True
                        )

            embed.set_footer(text="※同じ日は同じ結果になります（翌日更新）")
            await channel.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Botが起動しました！ ログイン中: {bot.user}")
    daily_omikuji.start()   # ←ここでループ開始

async def on_ready():
    print(f"Botが起動しました！ ログイン中: {bot.user}")
    daily_omikuji.start()

# トークンを貼り付ける
bot.run(TOKEN)
