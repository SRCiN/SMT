import discord
from discord.ext import commands, tasks
import asyncio
import hcskr
import aiosqlite
import datetime
from pytz import timezone, utc
import locale
import typing
locale.setlocale(locale.LC_ALL, '')

class Management(commands.Cog, name="Management"):
    def __init__(self, SMT):
        self.SMT = SMT
        self.health_check.start()

    @tasks.loop(seconds=60)
    async def health_check(self):
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        kortime = time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        debug = self.SMT.get_channel(783621627875164230)
        if "07시 30분" in kortime:
            await debug.send("시간 됐다. 그럼 시작해볼까?")
            o = await aiosqlite.connect("SMT.db")
            c = await o.cursor()
            await c.execute("SELECT * FROM health")
            rows = await c.fetchall()
            success = 0
            for row in rows:
                user = self.SMT.get_user(int(row[0]))
                hcs = await hcskr.asyncTokenSelfCheck(row[1])
                if hcs['code'] == "SUCCESS":
                    success += 1
                    if row[2] == "true":
                        embed = discord.Embed(title="완료했어! 좋은 하루 보내.", description=f"이렇다는데, 솔직히 잘 모르겠어.\n```{hcs['code']} : {hcs['message']}```", color=0x1F44BF, timestamp=datetime.datetime.utcnow())
                        embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format="png", size=2048))
                        embed.set_footer(text="Project. SMT v1.2.1")
                        try:
                            await user.send(user.mention, embed=embed)
                        except:
                            print("DM Failed.")
                else:
                    embed = discord.Embed(title="미안해, 뭔가 잘못된 거 같아.", description=f"내가 기대했던 결과랑 좀 다른 것 같은데.\n```{hcs['code']} : {hcs['message']}```", color=0xBE1010, timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format="png", size=2048))
                    embed.set_footer(text="Project. SMT v1.2.1")
                    try:
                        await user.send(user.mention, embed=embed)
                    except:
                        print("DM Failed.")
            await debug.send(f"다 됐어! 이번 시도에서는...\n{len(rows)}명을 시도했어.\n성공은 {success}명, 실패는 {len(rows) - success}명이야!")
            await o.close()

    @health_check.before_loop
    async def status_update_wait(self):
        print("봇 준비 대기 중")
        await self.SMT.wait_until_ready()

    @commands.command(name="닉네임")
    @commands.has_role(719061173567488010)
    async def _force(self, ctx, member: discord.Member, *, name):
        if member == ctx.author:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 미안, 너 스스로는 닉네임을 변경할 수 없어.")
        elif member == ctx.guild.owner:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 아, 그 사람은 나도 못 바꿔줘. 유일하게 내가 바꾸지 못하는 사람이라 해야하나?")
        else:
            embed = discord.Embed(title="잠깐만, 진짜로 하게?", description=f"다른 사람의 닉네임을 바꿀 때는 조심하는 게 좋을텐데.\n{member.mention}의 닉네임을 **{name}**으로 바꿔도 되는 거 맞지?", color=0xBE1010, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format='png', size=2048))
            embed.set_footer(text="Project. SMT v1.2.1")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("<:cs_yes:659355468715786262>")
            await msg.add_reaction("<:cs_no:659355468816187405>")
            def check(reaction, user):
                return reaction.message.id == msg.id and user == ctx.author
            try:
                reaction, user = await self.SMT.wait_for('reaction_add', timeout=20, check=check)
            except asyncio.TimeoutError:
                return
            else:
                await msg.delete()
                if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                    await member.edit(nick=name)
                    try:
                        await member.send(f"<:cs_id:659355469034422282> {member.mention} - 관리자에 의해 서버 내에서의 너의 이름이 **{name}**으로 바뀌었어!")
                    except:
                        channel = self.SMT.get_channel(783598891496767488)
                        await channel.send(f"<:cs_id:659355469034422282> {member.mention} - 관리자에 의해 서버 내에서의 너의 이름이 **{name}**으로 바뀌었어!")
                    await ctx.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} - 일단은 하긴 했는데, **{member}**의 이름을 **{name}**(으)로 바꿔도 되는 거 맞아?")

    @commands.command(name="동결", aliases=["얼려", "얼려줘"])
    @commands.has_role(719061173567488010)
    async def _freeze(self, ctx):
        embed = discord.Embed(title="잠깐만, 진짜로 하게?", description=f"이 채널, 정말 메시지 기능을 제한해도 괜찮은거야?", color=0xBE1010, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format='png', size=2048))
        embed.set_footer(text="Project. SMT v1.2.1")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("<:cs_yes:659355468715786262>")
        await msg.add_reaction("<:cs_no:659355468816187405>")
        def check(reaction, user):
            return reaction.message.id == msg.id and user == ctx.author
        try:
            reaction, user = await self.SMT.wait_for('reaction_add', timeout=20, check=check)
        except asyncio.TimeoutError:
            return
        else:
            await msg.delete()
            if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                overwrite = discord.PermissionOverwrite(read_messages=False, send_messages=False)
                await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                await ctx.send(f":lock: {ctx.author.mention} - 음, 그래? 네가 괜찮다면야. 이 채널의 메시지 기능을 제한해둘게.")
                    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 705282939365359616:
            vc = member.guild.get_channel(760549983606407189)
            await vc.edit(name=f"{member.guild.member_count}개의 계정", reason="어서 와! 만나서 반가워!")
            role = member.guild.get_role(749219515224686593)
            role2 = member.guild.get_role(749219945732112444)
            await member.add_roles(role, role2, reason="어서 와! 만나서 반가워!")
            if member.bot:
                bot_role = member.guild.get_role(749214540327026719)
                await member.add_roles(bot_role, reason="뭐야, 기계였잖아? 괜히 인사했네.")
            else:
                try:
                    embed = discord.Embed(title="안녕, 만나서 반가워!", description=f"{member.mention}이라고 부르면 될까?\n이 서버는 제한된 유저만이 접근할 수 있어서, 승인이 꼭 필요해.", color=0xBE1010, timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="초대한 사람이 뭔가 알려주던데.. 그건 뭐에요?", value="아, 코드를 받았구나! 그럼 빠르게 넘어가보자고! <#719058190175698964> 채널에서 `라더님 리퀘 단어` 명령어로 나한테 알려줄래?")
                    embed.add_field(name="저는 그런 거 못 받았어요! 어떻게 해요?", value="그럼 서버 관리자가 너를 확인하고 역할을 부여해줄 때까지만 기다려줘. 아마 관리자가 곧 확인하고 너에게 부여해줄 거야.")
                    embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format="png", size=2048))
                    embed.set_footer(text="Project. SMT v1.2.1")
                    await member.send(member.mention, embed=embed)
                except discord.Forbidden:
                    print("DM Failed.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 705282939365359616:
            vc = member.guild.get_channel(760549983606407189)
            await vc.edit(name=f"{member.guild.member_count}개의 계정", reason="잘 가. 다음에 또 보자!")

    @commands.command(name="알려")
    @commands.is_owner()
    async def _notify(self, ctx, channel: discord.TextChannel, *, message):
        await channel.send(message)
        await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
    
    @commands.command(name="자가진단")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def manage_health(self, ctx, todo):
        await ctx.message.delete()
        o = await aiosqlite.connect("SMT.db")
        c = await o.cursor()
        await c.execute(f"SELECT * FROM health WHERE user_id = {ctx.author.id}")
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
                        msg = await self.SMT.wait_for('message', timeout=30, check=check)
                    except asyncio.TimeoutError:
                        await queue.edit(content=f":hourglass: {ctx.author.mention} - 아, 미안해. 바빠서 못 들었어. 다시 해줄래?", delete_after=3)
                        break
                    else:
                        await msg.delete()
                        await queue.delete()
                        info.append(str(msg.content))
                        i += 1
                asdf = await ctx.send(f"<:cs_id:659355469034422282> {ctx.author.mention} - 잠시만, 확인 좀 해보고.\n자가진단 테스트 : <a:cs_wait:659355470418411521> 진행 중")
                try:
                    hcs = await hcskr.asyncSelfCheck(name=info[0], birth=info[1], level=info[2], area=info[3], schoolname=info[4], customloginname=info[5], password=info[6])
                except Exception as e:
                    debug = self.SMT.get_channel(783621627875164230)
                    await debug.send(f"도와주고 있는데, 문제가 좀 생긴 것 같아. 네가 확인해줄래? ```{e}```")
                    await asdf.edit(content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 음, 실패한 것 같네.\n자가진단 테스트 : <:cs_no:659355468816187405> 실패\n \n뭔가 잘못 실행된 거 같아. ```{e}```", delete_after=5)
                else:
                    await asyncio.sleep(1)
                    if hcs['code'] != "SUCCESS":
                        debug = self.SMT.get_channel(783621627875164230)
                        await debug.send(f"도와주고 있는데, 문제가 좀 생긴 것 같아. 네가 확인해줄래? ```{hcs['code']} : {hcs['message']}```")
                        await asdf.edit(content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 음, 실패한 것 같네.\n자가진단 테스트 : <:cs_no:659355468816187405> 실패\n \n내가 생각했던 것과는 뭔가 다른 답을 받았네. ```{hcs['code']} : {hcs['message']}```", delete_after=5)
                    else:
                        await asdf.edit(content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 거의 다 됐는데..\n자가진단 테스트 : <:cs_yes:659355468715786262> 완료\nSQLite 시스템에 등록 : <a:cs_wait:659355470418411521> 진행 중")
                        await asyncio.sleep(1)
                        try:
                            hcs_token = await hcskr.asyncGenerateToken(name=info[0], birth=info[1], level=info[2], area=info[3], schoolname=info[4], customloginname=info[5], password=info[6])
                            await c.execute(f"INSERT INTO health(user_id, token, notify) VALUES('{ctx.author.id}', '{hcs_token['token']}', 'true')")
                            await o.commit()
                        except Exception as e:
                            debug = self.SMT.get_channel(783621627875164230)
                            await debug.send(f"도와주고 있는데, 문제가 좀 생긴 것 같아. 네가 확인해줄래? ```{e}```")
                            await asdf.edit(content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 음, 실패한 것 같네.\n자가진단 테스트 : <:cs_yes:659355468715786262> 완료\nSQLite 시스템에 등록 : <:cs_no:659355468816187405> 실패\n \n음, 등록이 안 된 거 같네. 다시 해볼래? ```{e}```", delete_after=5)
                        else:
                            await asdf.edit(content=f"<:cs_id:659355469034422282> {ctx.author.mention} - 다 됐어!\n자가진단 테스트 : <:cs_yes:659355468715786262> 완료\nSQLite 시스템에 등록 : <:cs_yes:659355468715786262> 완료\n \n<:cs_sent:659355469684539402> 등록 다 됐어! 매일 7시 30분에 자가진단을 내가 대신 해줄거야.", delete_after=5)
            else:
                await ctx.send(f"<:cs_id:659355469034422282> {ctx.author.mention} - 이미 등록해둔 거로 기억하는데.. 프로필이 바뀌었으면 삭제하고 다시 등록해줄래?")
        elif todo == "삭제":
            if rows:
                await c.execute(f"DELETE FROM health WHERE user_id = '{ctx.author.id}'")
                await o.commit()
                await ctx.send(f"<:cs_trash:659355468631769101> {ctx.author.mention} - 더 이상 필요없는 기능이야? 삭제는 해뒀어. 언제든 다시 등록할 수 있어!")
            else:
                await ctx.send(f"<:cs_id:659355469034422282> {ctx.author.mention} - 삭제해주고는 싶은데, 네 정보가 여기에는 없는 거 같아.")
        elif todo == "알림":
            if rows:
                if rows[0][8] == "true":
                    await c.execute(f"UPDATE health SET notify = 'false' WHERE user_id = '{ctx.author.id}'")
                    await o.commit()
                    await ctx.send(f"<:cs_off:659355468887490560> {ctx.author.mention} - 아, 알림 안 받을 거야? 체크해둘게.")
                else:
                    await c.execute(f"UPDATE health SET notify = 'true' WHERE user_id = '{ctx.author.id}'")
                    await o.commit()
                    await ctx.send(f"<:cs_on:659355468682231810> {ctx.author.mention} - 알았어, 아침에 자가진단 알림을 보내줄게!")
            else:
                await ctx.send(f"<:cs_id:659355469034422282> {ctx.author.mention} - 알림 설정은 먼저 네 프로필을 등록하고 바꿔줄래?")
        else:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 어, 그게 아니었던 것 같은데. 다시 생각해보는 건 어때?")
        await o.close()

    @commands.command(name="청소", aliases=["삭제"])
    @commands.has_role(719061173567488010)
    async def _purge(self, ctx, purge: int):
        if purge < 1 or purge > 100:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 어, 그게 아니었던 것 같은데. 다시 생각해보는 건 어때?")
        else:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=purge)
            await ctx.send(f"<:cs_trash:659355468631769101> {ctx.author.mention} - **{len(deleted)}**개의 메시지를 없애주면 되는 거, 맞아?", delete_after=5)

    @commands.command(name="DB")
    @commands.is_owner()
    async def _database(self, ctx, todo, *, command):
        o = await aiosqlite.connect("SMT.db")
        c = await o.cursor()
        if todo == "commit":
            await c.execute(command)
            await o.commit()
            await o.close()
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        elif todo == "fetch":
            await c.execute(command)
            a = ""
            rows = await c.fetchall()
            for row in rows:
                a += f"{row}\n"
            if len(a) <= 2000:
                await ctx.send(a)
            else:
                print(a)
                await ctx.send(a[:2000])
            await o.close()
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        else:
            await o.close()
            await ctx.message.add_reaction("<:cs_trash:659355468631769101>")

    @commands.command(name="슬로우", aliases=["슬로우모드"])
    @commands.has_role(719061173567488010)
    async def _slowmode(self, ctx, number: int):
        await ctx.message.delete()
        if number == 0:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send(f":stopwatch: {ctx.author.mention} - 알았어! 시원시원하게 가보자고!")
        elif number > 21600 or number <= 0:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 어, 그게 아니었던 것 같은데. 다시 생각해보는 건 어때?")
        else:
            if number <= 30:
                await ctx.channel.edit(slowmode_delay=number)
                await ctx.send(f":hourglass: {ctx.author.mention} - 가끔은 느린 게 필요할 때도 있겠지. **{number}**초 정도면 적당한 것 같아?")
            else:
                embed = discord.Embed(title="잠깐만, 진짜로 하게?", description=f"보통 그렇게까지 느리게 할 필요는 없긴 한데, 하겠다면 말리진 않을게.\n진짜로 이 채널의 딜레이를 **{number}**초로 바꿀거야?", color=0xBE1010, timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format='png', size=2048))
                embed.set_footer(text="Project. SMT v1.2.1")
                msg = await ctx.send(embed=embed)
                await msg.add_reaction("<:cs_yes:659355468715786262>")
                await msg.add_reaction("<:cs_no:659355468816187405>")
                def check(reaction, user):
                    return reaction.message.id == msg.id and user == ctx.author
                try:
                    reaction, user = await self.SMT.wait_for('reaction_add', timeout=20, check=check)
                except asyncio.TimeoutError:
                    return
                else:
                    await msg.delete()
                    if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                        await ctx.channel.edit(slowmode_delay=number)
                        await ctx.send(f":hourglass: {ctx.author.mention} - 이렇게까지 느린 걸 원하지는 않았지만, **{number}**초로 바꿔두긴 할게.")

    @commands.command(name="내보내", aliases=["킥", "추방"])
    @commands.has_role(719061173567488010)
    async def _kick(self, ctx, member: discord.Member, *, reason: typing.Optional[str] = "사유 없음."):
        await ctx.message.delete()
        if member.top_role < ctx.guild.me.top_role and member != ctx.guild.owner:
            try:
                await member.send(f"<a:ban_cat:761149577444720640> {ctx.author.mention} - 미안하지만, **{ctx.guild.name}**에서 내보내졌어. 다음에 다시 들어올 수 있으니까 걱정하진 말고.\n이유는 이렇다고 들었어. {reason}")
            except:
                print("Kick DM Failed.")
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f"<a:ban_cat:761149577444720640> {ctx.author.mention} - **{member}**를 내보내면 되는거야? 어딘가 불안한데..\n이게 이유 맞지? {reason}")
        else:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 어, 그게 아니었던 것 같은데. 다시 생각해보는 건 어때?")
        
    @commands.command(name="차단", aliases=["밴", "벤"])
    @commands.has_role(719061173567488010)
    async def _ban(self, ctx, user: discord.Member, delete: typing.Optional[int] = 0, *, reason: typing.Optional[str] = "사유 없음."):
        await ctx.message.delete()
        if user.top_role < ctx.guild.me.top_role and user != ctx.guild.owner:
            try:
                await user.send(f"<a:ban_guy:761149578216603668> {ctx.author.mention} - 미안하지만, **{ctx.guild.name}**에 다시 접속할 수 없게 되었어, 유감이네.\n이유는 이렇다고 들었어. {reason}")
            except:
                print("Ban DM Failed.")
            await ctx.guild.ban(user, delete_message_days=delete, reason=reason)
            await ctx.send(f"<a:ban_guy:761149578216603668> {ctx.author.mention} - **{user}**의 접속을 막으면 되는거 맞아? 이거 좀 이상한데..\n최근 {delete}일의 메시지를 삭제했어.\n이게 이유 맞지? {reason}")
        else:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 어, 그게 아니었던 것 같은데. 다시 생각해보는 건 어때?")

    @commands.command(name="역할", aliases=["이거"])
    @commands.has_role(719061173567488010)
    async def _role(self, ctx, member: discord.Member, *, what):
        await ctx.message.delete()
        if ctx.guild.id == 705282939365359616:
            o = await aiosqlite.connect("SMT.db")
            c = await o.cursor()
            await c.execute(f"SELECT * FROM roles WHERE name = '{what}'")
            rows = await c.fetchall()
            if not rows:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 어, 그게 아니었던 것 같은데. 다시 생각해보는 건 어때?")
            else:
                role = ctx.guild.get_role(int(rows[0][0]))
                if role not in member.roles:
                    await member.add_roles(role, reason="관리자에 의해 지급됨")
                    await ctx.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} - **{member}**에게 `{role.name}` 역할을 주면 되는 거지? 알았어!")
                else:
                    await member.remove_roles(role, reason="관리자에 의해 삭제됨")
                    await ctx.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} - **{member}**가 가지고 있던 `{role.name}` 역할을 다시 돌려놨어!")
            await o.close()
        else:
            await ctx.send(f'<:cs_no:659355468816187405> {ctx.author.mention} - 음, 모르겠네? 여기가 아니었던 거 같은데..')

    @commands.command(name="리퀘", aliases=["요청", "내놔"])
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def _request(self, ctx, *, code):
        await ctx.message.delete()
        if ctx.guild.id == 705282939365359616:
            o = await aiosqlite.connect("SMT.db")
            c = await o.cursor()
            await c.execute(f"SELECT * FROM roles WHERE code = '{code}'")
            rows = await c.fetchall()
            if not rows:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 미안해, 네가 말해준 역할을 찾을 수가 없어서 말이야. 다른 걸로 다시 해줄래?")
            else:
                if rows[0][3] == "true":
                    role = ctx.guild.get_role(int(rows[0][0]))
                    await ctx.author.add_roles(role, reason="리퀘스트를 통해 지급됨")
                    await ctx.author.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} - 아, 그 역할? 너한테 지급해줬어! `{role.name}`, 맞지?")
                else:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 미안해, 네가 말해준 역할을 찾을 수가 없어서 말이야. 다른 걸로 다시 해줄래?")
            await o.close()
        else:
            await ctx.send(f'<:cs_no:659355468816187405> {ctx.author.mention} - 음, 모르겠네? 여기가 아니었던 거 같은데..')

    @commands.command(name="커맨드")
    async def _command_management(self, ctx, todo, name, *, value: typing.Optional[str] = None):
        if "'" in ctx.message.content or '"' in ctx.message.content or "\\" in ctx.message.content or "@everyone" in ctx.message.content or "@here" in ctx.message.content:
            return await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 미안하지만, 이 명령어는 이상한 사람을 막기 위해 어떤 단어들을 사용할 수 없어.")
            
        o = await aiosqlite.connect("SMT.db")
        c = await o.cursor()
        await c.execute(f"SELECT * FROM `words` WHERE `name` = '{name}'")
        rows = await c.fetchall()
        if todo == "추가":
            if value is not None:
                if not rows:
                    embed = discord.Embed(title="잠깐만, 그거 정말 맞아?", description=f"`{name}`(이)라고 물어보면 이렇게 말해주면 되는 거 맞지?\n```{value}```", color=0xBE1010, timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format='png', size=2048))
                    embed.set_footer(text="Project. SMT v1.2.1")
                    msg = await ctx.send(ctx.author.mention, embed=embed)
                    await msg.add_reaction("<:cs_yes:659355468715786262>")
                    await msg.add_reaction("<:cs_no:659355468816187405>")
                    def check(reaction, user):
                        return reaction.message.id == msg.id and user == ctx.author
                    try:
                        reaction, user = await self.SMT.wait_for('reaction_add', timeout=20, check=check)
                    except asyncio.TimeoutError:
                        await msg.delete()
                    else:
                        if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                            await msg.delete()
                            await c.execute(f"INSERT INTO words(name, value, teachedBy, locked) VALUES('{name}', '{value}', '{ctx.author.id}', 'false')")
                            await o.commit()
                            await ctx.send(f"➕ {ctx.author.mention} - 알았어! `{name}` 단어를 기억해둘게.")
                        else:
                            await msg.delete()
                else:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 그건 이미 있는 거 같은데, 수정하고 싶으면 수정해도 되고.")
            else:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 어, 그게 아니었던 것 같은데. 다시 생각해보는 건 어때?")
        elif todo == "수정":
            if value is not None:
                if rows:
                    if rows[0][3] != 'true':
                        embed = discord.Embed(title="잠깐만, 그거 정말 맞아?", description=f"`{name}`(이)라고 물어보면 이렇게 말해주면 되는 거 맞지?\n```{value}```", color=0xBE1010, timestamp=datetime.datetime.utcnow())
                        embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format='png', size=2048))
                        embed.set_footer(text="Project. SMT v1.2.1")
                        msg = await ctx.send(ctx.author.mention, embed=embed)
                        await msg.add_reaction("<:cs_yes:659355468715786262>")
                        await msg.add_reaction("<:cs_no:659355468816187405>")
                        def check(reaction, user):
                            return reaction.message.id == msg.id and user == ctx.author
                        try:
                            reaction, user = await self.SMT.wait_for('reaction_add', timeout=20, check=check)
                        except asyncio.TimeoutError:
                            await msg.delete()
                        else:
                            if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                                await msg.delete()
                                await c.execute(f"UPDATE words SET value = '{value}' WHERE name = '{name}'")
                                await c.execute(f"UPDATE words SET teachedBy = '{ctx.author.id}' WHERE name = '{name}'")
                                await o.commit()
                                await ctx.send(f"<:cs_reboot:659355468791283723> {ctx.author.mention} - 알았어! `{name}` 단어를 다시 기억해둘게.")
                            else:
                                await msg.delete()
                    else:
                        await ctx.send(f":lock: {ctx.author.mention} - 어, 그 단어는 잠금 설정되어 있어. 다른 걸 수정해볼래?")
                else:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 네가 말해준 단어를 찾지 못했어. 다른 걸로 해볼래?")
            else:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 어, 그게 아니었던 것 같은데. 다시 생각해보는 건 어때?")
        elif todo == "삭제":
            if rows:
                if rows[0][3] != 'true':
                    embed = discord.Embed(title="잠깐만, 그거 정말 맞아?", description=f"`{name}`(이)라고 물어봐도 모른 척 하면 되는거야?", color=0xBE1010, timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format='png', size=2048))
                    embed.set_footer(text="Project. SMT v1.2.1")
                    msg = await ctx.send(ctx.author.mention, embed=embed)
                    await msg.add_reaction("<:cs_yes:659355468715786262>")
                    await msg.add_reaction("<:cs_no:659355468816187405>")
                    def check(reaction, user):
                        return reaction.message.id == msg.id and user == ctx.author
                    try:
                        reaction, user = await self.SMT.wait_for('reaction_add', timeout=20, check=check)
                    except asyncio.TimeoutError:
                        await msg.delete()
                    else:
                        if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                            await msg.delete()
                            await c.execute(f"DELETE FROM words WHERE name = '{name}'")
                            await o.commit()
                            await ctx.send(f"<:cs_trash:659355468631769101> {ctx.author.mention} - 알았어! `{name}` 단어를 잊어버리게 뭐, 노력은 해볼게.")
                        else:
                            await msg.delete()
                else:
                    await ctx.send(f":lock: {ctx.author.mention} - 어, 그 단어는 잠금 설정되어 있어. 다른 걸 삭제해볼래?")
            else:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 네가 말해준 단어를 찾지 못했어. 다른 걸로 해볼래?")
        elif todo == "잠금":
            staff = ctx.guild.get_role(719061173567488010)
            if staff in ctx.author.roles:
                if rows:
                    if rows[0][3] != 'true':
                        embed = discord.Embed(title="잠깐만, 그거 정말 맞아?", description=f"`{name}` 단어를 아무도 바꾸지 못하게 할건데, 괜찮아?", color=0xBE1010, timestamp=datetime.datetime.utcnow())
                        embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format='png', size=2048))
                        embed.set_footer(text="Project. SMT v1.2.1")
                        msg = await ctx.send(ctx.author.mention, embed=embed)
                        await msg.add_reaction("<:cs_yes:659355468715786262>")
                        await msg.add_reaction("<:cs_no:659355468816187405>")
                        def check(reaction, user):
                            return reaction.message.id == msg.id and user == ctx.author
                        try:
                            reaction, user = await self.SMT.wait_for('reaction_add', timeout=20, check=check)
                        except asyncio.TimeoutError:
                            await msg.delete()
                        else:
                            if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                                await msg.delete()
                                await c.execute(f"UPDATE words SET locked = 'true' WHERE name = '{name}'")
                                await o.commit()
                                await ctx.send(f":lock: {ctx.author.mention} - 그래, 뭐. 괜찮다면야. `{name}` 단어를 제한해둘게.")
                            else:
                                await msg.delete()
                    else:
                        await ctx.send(f":lock: {ctx.author.mention} - 이미 잠겨 있는 단어라서 의미 없어 보이는데.")
                else:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 네가 말해준 단어를 찾지 못했어. 다른 걸로 해볼래?")
            else:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 그건 어떤 역할을 가지고 있는 사람만 사용할 수 있어. 다음에 다시 해줄래?")
        elif todo == "해제":
            staff = ctx.guild.get_role(719061173567488010)
            if staff in ctx.author.roles:
                if rows:
                    if rows[0][3] != 'false':
                        embed = discord.Embed(title="잠깐만, 그거 정말 맞아?", description=f"`{name}` 단어를 누구나 바꿀 수 있게 될 거야. 상관 없지?", color=0xBE1010, timestamp=datetime.datetime.utcnow())
                        embed.set_thumbnail(url=self.SMT.user.avatar_url_as(format='png', size=2048))
                        embed.set_footer(text="Project. SMT v1.2.1")
                        msg = await ctx.send(ctx.author.mention, embed=embed)
                        await msg.add_reaction("<:cs_yes:659355468715786262>")
                        await msg.add_reaction("<:cs_no:659355468816187405>")
                        def check(reaction, user):
                            return reaction.message.id == msg.id and user == ctx.author
                        try:
                            reaction, user = await self.SMT.wait_for('reaction_add', timeout=20, check=check)
                        except asyncio.TimeoutError:
                            await msg.delete()
                        else:
                            if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                                await msg.delete()
                                await c.execute(f"UPDATE words SET locked = 'false' WHERE name = '{name}'")
                                await o.commit()
                                await ctx.send(f":unlock: {ctx.author.mention} - 그래, 뭐. `{name}` 단어의 제한을 풀어 놓을게.")
                            else:
                                await msg.delete()
                    else:
                        await ctx.send(f":unlock: {ctx.author.mention} - 그거 딱히 내가 제한 걸어놓은 적 없던 거 같은데, 상관 없으려나.")
                else:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 네가 말해준 단어를 찾지 못했어. 다른 걸로 해볼래?")
            else:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 그건 어떤 역할을 가지고 있는 사람만 사용할 수 있어. 다음에 다시 해줄래?")
        await o.close()
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            o = await aiosqlite.connect("SMT.db")
            c = await o.cursor()
            name = ctx.message.content.split(" ")[1]
            await c.execute(f"SELECT * FROM words WHERE name = '{name}'")
            rows = await c.fetchall()
            if rows:
                user = self.SMT.get_user(int(rows[0][2]))
                await ctx.send(f"{rows[0][1]}\n \n`{user}`(이)라는 애가 알려준 건데, 무슨 문제라도 있어?")
            else:
                await ctx.message.delete()
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 잘 모르겠네. 맞게 입력했는지 다시 한번만 확인해줄래?")
            await o.close()

def setup(SMT):
    SMT.add_cog(Management(SMT))