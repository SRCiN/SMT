import discord
from discord.ext import commands

class Events(commands.Cog, name="Event Listeners):
    def __init__(self, SMT):
        self.SMT = SMT

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

def setup(SMT):
    SMT.add_cog(Events(SMT))
