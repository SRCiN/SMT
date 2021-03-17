import discord
from discord.ext import commands
import aiosqlite

class Global(commands.Cog, name="범용"):
    def __init__(self, SMT):
        self.SMT = SMT

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.SMT.user)
        print(self.SMT.user.id)
        print("Bot is READY.")
        await self.SMT.change_presence(status=discord.Status.idle, activity=discord.Game("너와 함께"), afk=True)

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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
                await ctx.send(f":mag_right: {ctx.author.mention} - `{error.argument}`(이)랑 관련된 사람을 못 찾았어. 확인하고 다시 해줄래?")
            elif isinstance(error, commands.ChannelNotFound):
                await ctx.send(f":mag_right: {ctx.author.mention} - `{error.argument}`(이)랑 관련된 채널을 못 찾았어. 확인하고 다시 해줄래?")
            elif isinstance(error, commands.ChannelNotReadable):
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - `{error.argument}`(이)랑 관련된 채널은 내가 접근할 수 없는 것 같아.")
            elif isinstance(error, commands.RoleNotFound):
                await ctx.send(f":mag_right: {ctx.author.mention} - `{error.argument}`(이)랑 관련된 역할을 못 찾았어. 확인하고 다시 해줄래?")
            else:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 어, 그게 아니었던 것 같은데. 다시 생각해보는 건 어때?")
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 미안해, 그 명령어는 아무나 사용할 수 없도록 제한되어 있어.")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 그건 어떤 역할을 가지고 있는 사람만 사용할 수 있어. 다음에 다시 해줄래?")
        elif isinstance(error, commands.MissingRole):
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 그건 어떤 역할을 가지고 있는 사람만 사용할 수 있어. 다음에 다시 해줄래?")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f":stopwatch: {ctx.author.mention} - 그건 좀 더 이따가 사용해줄래? {round(error.retry_after, 2)}초 정도 뒤면 될 거 같아.")
        else:
            developer = self.SMT.get_user(526958314647453706)
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 미안해, 뭔가 문제가 생긴 것 같아. **{developer}**한테 한번 물어봐줄래?")
            channel = self.SMT.get_channel(783621627875164230)
            await channel.send(f'도와주고 있는데, 문제가 좀 생긴 것 같아. 네가 확인해줄래? ```{error}```')

def setup(SMT):
    SMT.add_cog(Global(SMT))
