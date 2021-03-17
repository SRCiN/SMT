import discord
from discord.ext import commands
import aiosqlite
import datetime

class Miya(commands.Cog, name="미야 관리"):
    def __init__(self, SMT):
        self.SMT = SMT

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        now = datetime.datetime.utcnow()
        delay = now - member.joined_at
        limit = datetime.datetime(2020, 8, 22) - datetime.datetime(2020, 8, 17)
        text = str(delay).split(".")[0]
        if delay <= limit:
            filter = [
                "시발",
                "ㅅㅂ",
                "ㅆㅃ",
                "ㅆㅂ",
                "병신",
                "ㅂㅅ",
                "개새끼",
                "애미",
                "애비",
                "느금마",
                "ㄴㄱㅁ",
            ]
            for word in filter:
                if word in msg.content and msg.channel.id != 663806592277545005:
                    try:
                        await msg.author.send(f"<:cs_stop:665173353874587678> {msg.author.mention} - 서버에 접속해 있었던 기간이 5일 미만이고, {text}일 부적절한 언행을 사용하셔서 차단되셨습니다.")
                    except:
                        await msg.reply(f"<:cs_stop:665173353874587678> 서버에 접속해 있었던 기간이 5일 미만이고, {text}일 부적절한 언행을 사용하셔서 차단당했습니다.")
                    await msg.guild.ban(msg.author, delete_message_days=7, reason="서버 활동 기간이 5일 미만이고, 부적절한 언행을 사용했습니다.")

    @commands.Cog.listener()
    async def on_member_join(member):
        if member.bot:
            return

        if member.guild.id == 564418977627897887:
            now = datetime.datetime.utcnow()
            delay = now - member.created_at
            limit = datetime.datetime(2020, 8, 20) - datetime.datetime(2020, 8, 17)
            text = str(delay).split(".")[0]
            if delay <= limit:
                try:
                    await member.send(f"<:cs_stop:665173353874587678> {member.mention} - 지원 서버 정책에 따라, 생성된 지 3일이 되지 않은 계정은 추방됩니다.")
                except:
                    channel = self.SMT.get_channel(694761306250674207)
                    await channel.send(f"<:cs_stop:665173353874587678> {member.mention} - 지원 서버 정책에 따라, 생성된 지 3일이 되지 않은 계정은 추방됩니다.")
                    await asyncio.sleep(3)
                await member.guild.kick(member, reason="계정이 활동한 기간이 너무 짧습니다!")

class Ticket(commands.Cog, name="티켓 지원 시스템"):
    def __init__(self, SMT):
        self.SMT = SMT
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        if str(payload.emoji) == "<:cs_leave:659355468803866624>" and payload.guild_id == 564418977627897887:
            g = self.SMT.get_guild(payload.guild_id)
            ch = g.get_channel(payload.channel_id)
            if ch.name.startswith("티켓_"):
                member = g.get_member(int(ch.topic))
                await ch.set_permissions(member, overwrite=None)
                name = ch.name.replace("티켓", "종료")
                await ch.edit(name=name)
                try:
                    await member.send(f"<:cs_leave:659355468803866624> {member.mention} - 당신이 열었던 티켓이 닫혔어요. 다시 여시려면 `상어 티켓 [ 채널 ID ]`를 사용해주세요.\n채널 ID : {ch.id}")
                except:
                    print("Discord 개인 메시지가 차단되어 전송하지 않았습니다.")
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        
        if msg.channel.id == 663806592277545005:
            await msg.delete()
            category = msg.guild.get_channel(821698815944818708)
            overwrites = {
                msg.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                msg.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True, manage_roles=True)
            }
            o = await aiosqlite.connect("SMT.db")
            c = await o.cursor()
            await c.execute("SELECT * FROM shark")
            rows = await c.fetchall()
            number = ""
            for i in range(len(str(rows[0][1])), 4):
                number += "0"
            number += str(rows[0][1])
            channel = await category.create_text_channel(name=f"티켓_{number}", overwrites=overwrites, topic=msg.author.id)
            embed = discord.Embed(title=f"{msg.author}님의 새 문의 채널", description=f"사유 : {msg.content}\n티켓을 닫으려면 아래에 있는 반응을 누르세요.", color=0xAFFDEF, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=msg.author.avatar_url_as(static_format="png", size=2048))
            embed.set_footer(text="티켓을 통한 지원 시스템", icon_url=self.SMT.user.avatar_url)
            msg = await channel.send("@here", embed=embed)
            await msg.add_reaction("<:cs_leave:659355468803866624>")
            await msg.pin()
            await c.execute(f'UPDATE shark SET ticket = {int(rows[0][1]) + 1}')
            await o.commit()
            await o.close()
    
    @commands.command(name="티켓")
    async def _reopen(self, ctx, channel: discord.TextChannel):
        if channel.name.startswith("종료_"):
            if ctx.author.id == channel.topic or ctx.author.top_role.id == 659351693481345034:
                member = ctx.guild.get_member(int(channel.topic))
                name = channel.name.replace("종료", "티켓")
                await channel.edit(name=name)
                overwrite = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True, manage_roles=True)
                await channel.set_permissions(member, overwrite=overwrite)
                message = None
                async for msg in channel.history(limit=500):
                    if msg.author == self.SMT.user:
                        message = msg
                await message.reply("<:cs_yes:659355468715786262> @here - 지원 티켓이 티켓 소유자 또는 서버 관리자에 의해 다시 활성화됐습니다.")
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")

def setup(SMT):
    SMT.add_cog(Ticket(SMT))
    SMT.add_cog(Miya(SMT))
