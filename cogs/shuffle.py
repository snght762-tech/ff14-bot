import disnake
from disnake.ext import commands
import random
import re
from typing import Optional

from utils.emojis import emoji_map

# 人数ごとのロール枠
role_distribution = {
    8: {"Tank": 2, "Healer": 2, "DPS": 4},
    4: {"Tank": 1, "Healer": 1, "DPS": 2}
}

# メンション文字列からメンバーを抽出
def extract_members(raw_text, guild):
    # メンションIDを抽出（ダブルクォーテーションなしでもOK）
    member_ids = re.findall(r"<@!?(\d+)>", raw_text)
    return [guild.get_member(int(uid)) for uid in member_ids if guild.get_member(int(uid))]

# 完全ランダム割り当て
def assign_jobs(members, role_dist):
    assignments = {}
    used_jobs = set()

    member_list = random.sample(members, len(members))

    role_slots = []
    for role, count in role_dist.items():
        role_slots.extend([role] * count)
    random.shuffle(role_slots)

    for role in role_slots:
        if not member_list:
            break
        member = member_list.pop(0)
        available_jobs = [j for j in emoji_map[role]["jobs"].keys() if j not in used_jobs]
        job = random.choice(available_jobs)
        assignments[member] = (role, job)
        used_jobs.add(job)

    return assignments


class Shuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="FF14 ジョブルーレット 🎲")
    async def shuffle(
        self,
        inter: disnake.ApplicationCommandInteraction,
        size: int,
        mode: Optional[str] = commands.Param(choices=["role"], default=None),
    ):
        await inter.response.defer()

        raw_input = inter.options["members"]
        member_list = extract_members(raw_input, inter.guild)
        if not member_list:
            await inter.edit_original_response("有効なメンバーが見つかりませんでした。")
            return

        role_dist = role_distribution.get(size, {"Tank": 2, "Healer": 2, "DPS": 4})
        assignments = assign_jobs(member_list, role_dist)

        result_text = ""
        for member, (role, job) in assignments.items():
            emoji_role = emoji_map[role][role]
            if mode == "role":
                result_text += f"{member.display_name}\n{emoji_role} {role}\n\n"
            else:
                emoji_job = emoji_map[role]["jobs"][job]
                result_text += f"{member.display_name}\n{emoji_role} {role} → {emoji_job} {job}\n\n"

        embed = disnake.Embed(
            title="🎲 FF14 ランダムジョブ割り当て",
            description=result_text,
            color=disnake.Color.blue(),
        )
        embed.set_footer(text=f"Tank: {role_dist.get('Tank', 0)} / Healer: {role_dist.get('Healer', 0)} / DPS: {role_dist.get('DPS', 0)}")

        await inter.edit_original_response(embed=embed)


def setup(bot):
    bot.add_cog(Shuffle(bot))