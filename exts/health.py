import asyncio
import datetime
import locale

import aiosqlite
import discord
import hcskr
from discord.ext import commands
from discord.ext import tasks
from pytz import timezone
from pytz import utc

locale.setlocale(locale.LC_ALL, "")


class Health(commands.Cog, name="자동 자가진단"):
    def __init__(self, SMT):
        self.SMT = SMT
        self.health_check.start()

    @tasks.loop(seconds=60)
    async def health_check(self):
        KST = timezone("Asia/Seoul")
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        kortime = time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        debug = self.SMT.get_channel(783621627875164230)
        if "07시 00분" in kortime:
            await debug.send("시간 됐다. 그럼 시작해볼까?")
            o = await aiosqlite.connect("SMT.db")
            c = await o.cursor()
            await c.execute("SELECT * FROM health")
            rows = await c.fetchall()
            success = 0
            for row in rows:
                user = self.SMT.get_user(int(row[0]))
                hcs = await hcskr.asyncTokenSelfCheck(row[1])
                if hcs["code"] == "SUCCESS":
                    success += 1
                    if row[2] == "true":
                        embed = discord.Embed(
                            title="완료했어! 좋은 하루 보내.",
                            description=f"이렇다는데, 솔직히 잘 모르겠어.\n```{hcs['code']} : {hcs['message']}```",
                            color=0x1F44BF,
                            timestamp=datetime.datetime.utcnow(),
                        )
                        embed.set_thumbnail(url=self.SMT.user.avatar_url_as(
                            format="png", size=2048))
                        embed.set_footer(text="Project. SMT v1.4")
                        try:
                            await user.send(user.mention, embed=embed)
                        except:
                            print("DM Failed.")
                else:
                    embed = discord.Embed(
                        title="미안해, 뭔가 잘못된 거 같아.",
                        description=f"내가 기대했던 결과랑 좀 다른 것 같은데.\n```{hcs['code']} : {hcs['message']}```",
                        color=0xBE1010,
                        timestamp=datetime.datetime.utcnow(),
                    )
                    embed.set_thumbnail(url=self.SMT.user.avatar_url_as(
                        format="png", size=2048))
                    embed.set_footer(text="Project. SMT v1.4")
                    try:
                        await user.send(user.mention, embed=embed)
                    except:
                        print("DM Failed.")
            await debug.send(
                f"다 됐어! 이번 시도에서는...\n{len(rows)}명을 시도했어.\n성공은 {success}명, 실패는 {len(rows) - success}명이야!"
            )
            await o.close()

    @health_check.before_loop
    async def status_update_wait(self):
        print("봇 준비 대기 중")
        await self.SMT.wait_until_ready()

    @commands.command(name="자가진단")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def manage_health(self, ctx, todo):
        await ctx.message.delete()
        o = await aiosqlite.connect("SMT.db")
        c = await o.cursor()
        await c.execute(f"SELECT * FROM health WHERE user_id = {ctx.author.id}"
                        )
        rows = await c.fetchall()
        if todo == "추가":
            if not rows:
                info = []
                i = 0
                while i < 7:
                    messages = [
                        f":stopwatch: {ctx.author.mention} - 이름이 뭐야? Ex) 홍길동",
                        f":stopwatch: {ctx.author.mention} - 생일을 좀 말해줄래? Ex) 자신이 2020년 12월 6일생이라면, `201206`",
                        f":stopwatch: {ctx.author.mention} - 학교급은 어떻게 돼? Ex) 초등학교, 중학교, 고등학교 등",
                        f":stopwatch: {ctx.author.mention} - 학교 지역은 어디야? Ex) 서울, 경기, 제주 등",
                        f":stopwatch: {ctx.author.mention} - 학교 이름을 좀 알려줄래? Ex) 세모고등학교, 네모초등학교 등",
                        f":stopwatch: {ctx.author.mention} - 누가 수행했다고 적어줄까? Ex) 홍길동, [자동] 홍길동 등",
                        f":stopwatch: {ctx.author.mention} - 자가진단을 해주기 위한 비밀번호를 말해줘. Ex) 1234",
                    ]
                    queue = await ctx.send(messages[i])

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    try:
                        msg = await self.SMT.wait_for("message",
                                                      timeout=30,
                                                      check=check)
                    except asyncio.TimeoutError:
                        await queue.edit(
                            content=f":hourglass: {ctx.author.mention} - 아, 미안해. 바빠서 못 들었어. 다시 해줄래?",
                            delete_after=3,
                        )
                        break
                    else:
                        await msg.delete()
                        await queue.delete()
                        info.append(str(msg.content))
                        i += 1
                asdf = await ctx.send(
                    f"<:cs_id:659355469034422282> {ctx.author.mention} - 잠시만, 확인 좀 해보고.\n자가진단 테스트 및 정보 암호화 : <a:cs_wait:659355470418411521> 진행 중"
                )
                try:
                    hcs_token = await hcskr.asyncGenerateToken(
                        name=info[0],
                        birth=info[1],
                        level=info[2],
                        area=info[3],
                        schoolname=info[4],
                        customloginname=info[5],
                        password=info[6],
                    )
                except Exception as e:
                    debug = self.SMT.get_channel(783621627875164230)
                    await debug.send(
                        f"도와주고 있는데, 문제가 좀 생긴 것 같아. 네가 확인해줄래? ```{e}```")
                    await asdf.edit(
                        content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 음, 실패한 것 같네.\n자가진단 테스트 및 정보 암호화 : <:cs_no:659355468816187405> 실패\n \n뭔가 잘못 실행된 거 같아. ```{e}```",
                        delete_after=5,
                    )
                else:
                    await asyncio.sleep(1)
                    if hcs_token["code"] != "SUCCESS":
                        debug = self.SMT.get_channel(783621627875164230)
                        await debug.send(
                            f"도와주고 있는데, 문제가 좀 생긴 것 같아. 네가 확인해줄래? ```{hcs_token['code']} : {hcs_token['message']}```"
                        )
                        await asdf.edit(
                            content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 음, 실패한 것 같네.\n자가진단 테스트 및 정보 암호화 : <:cs_no:659355468816187405> 실패\n \n내가 생각했던 것과는 뭔가 다른 답을 받았네. ```{hcs_token['code']} : {hcs_token['message']}```",
                            delete_after=5,
                        )
                    else:
                        await asdf.edit(
                            content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 거의 다 됐는데..\n자가진단 테스트 및 정보 암호화 : <:cs_yes:659355468715786262> 완료\nSQLite 시스템에 등록 : <a:cs_wait:659355470418411521> 진행 중"
                        )
                        await asyncio.sleep(1)
                        try:
                            await c.execute(
                                f"INSERT INTO health(user_id, token, notify) VALUES('{ctx.author.id}', '{hcs_token['token']}', 'true')"
                            )
                            await o.commit()
                        except Exception as e:
                            debug = self.SMT.get_channel(783621627875164230)
                            await debug.send(
                                f"도와주고 있는데, 문제가 좀 생긴 것 같아. 네가 확인해줄래? ```{e}```"
                            )
                            await asdf.edit(
                                content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 음, 실패한 것 같네.\n자가진단 테스트 및 정보 암호화 : <:cs_yes:659355468715786262> 완료\nSQLite 시스템에 등록 : <:cs_no:659355468816187405> 실패\n \n음, 등록이 안 된 거 같네. 다시 해볼래? ```{e}```",
                                delete_after=5,
                            )
                        else:
                            await asdf.edit(
                                content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 다 됐어!\n자가진단 테스트 및 정보 암호화 : <:cs_yes:659355468715786262> 완료\nSQLite 시스템에 등록 : <:cs_yes:659355468715786262> 완료\n \n<:cs_sent:659355469684539402> 등록 다 됐어! 매일 7시에 자가진단을 내가 대신 해줄거야.",
                                delete_after=5,
                            )
            else:
                await ctx.send(
                    f"<:cs_id:659355469034422282> {ctx.author.mention} - 이미 등록해둔 거로 기억하는데.. 프로필이 바뀌었으면 삭제하고 다시 등록해줄래?"
                )
        elif todo == "삭제":
            if rows:
                await c.execute(
                    f"DELETE FROM health WHERE user_id = '{ctx.author.id}'")
                await o.commit()
                await ctx.send(
                    f"<:cs_trash:659355468631769101> {ctx.author.mention} - 더 이상 필요없는 기능이야? 삭제는 해뒀어. 언제든 다시 등록할 수 있어!"
                )
            else:
                await ctx.send(
                    f"<:cs_id:659355469034422282> {ctx.author.mention} - 삭제해주고는 싶은데, 네 정보가 여기에는 없는 거 같아."
                )
        elif todo == "알림":
            if rows:
                if rows[0][2] == "true":
                    await c.execute(
                        f"UPDATE health SET notify = 'false' WHERE user_id = '{ctx.author.id}'"
                    )
                    await o.commit()
                    await ctx.send(
                        f"<:cs_off:659355468887490560> {ctx.author.mention} - 아, 알림 안 받을 거야? 체크해둘게."
                    )
                else:
                    await c.execute(
                        f"UPDATE health SET notify = 'true' WHERE user_id = '{ctx.author.id}'"
                    )
                    await o.commit()
                    await ctx.send(
                        f"<:cs_on:659355468682231810> {ctx.author.mention} - 알았어, 아침에 자가진단 알림을 보내줄게!"
                    )
            else:
                await ctx.send(
                    f"<:cs_id:659355469034422282> {ctx.author.mention} - 알림 설정은 먼저 네 프로필을 등록하고 바꿔줄래?"
                )
        else:
            raise commands.BadArgument
        await o.close()


def setup(SMT):
    SMT.add_cog(Health(SMT))
