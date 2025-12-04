import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

# .envからトークンを読み込む
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents設定
intents = disnake.Intents.default()
intents.message_content = True  # メッセージ履歴を扱うなら必要

# Bot本体
bot = commands.InteractionBot(intents=intents)

# Bot起動時イベント
@bot.event
async def on_ready():
    print(f"✅ Bot起動完了！ ログイン中: {bot.user}")

# Cogの自動ロード
initial_extensions = [
    "cogs.omikuji",
    "cogs.images",
    "cogs.ids",
    "cogs.alliance",
    "cogs.raid",
    "cogs.help"
]

for ext in initial_extensions:
    try:
        bot.load_extension(ext)
        print(f"🔹 Loaded {ext}")
    except Exception as e:
        print(f"❌ Failed to load {ext}: {e}")

# Bot実行
bot.run(TOKEN)