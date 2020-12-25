import discord
from discord.ext import commands
import datetime
import aiohttp
import ast
import os
import asyncio

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class Global(commands.Cog, name="범용"):
    def __init__(self, SMT):
        self.SMT = SMT

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.SMT.user)
        print(self.SMT.user.id)
        print("Bot is READY.")
        await self.SMT.change_presence(status=discord.Status.idle, activity=discord.Game("너와 함께"), afk=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
            
        if member.guild.id == 564418977627897887 or member.guild.id == 705282939365359616:
            now = datetime.datetime.utcnow()
            delay = now - member.created_at
            limit = datetime.datetime(2020, 8, 20) - datetime.datetime(2020, 8, 17)
            text = str(delay).split(".")[0]
            if delay <= limit:
                try:
                    await member.send(f"<:cs_stop:665173353874587678> {member.mention} - 서버 정책에 따라, 생성된 지 3일이 되지 않은 계정은 추방 처리됩니다!\n당신의 계정은 만든지 {text} 정도 지나고 있습니다. 나중에 다시 방문해주세요!")
                except:
                    channel = None
                    if member.guild.id == 564418977627897887:
                        channel = self.SMT.get_channel(694761306250674207)
                    elif member.guild.id == 705282939365359616:
                        channel = self.SMT.get_channel(719058190175698964)
                    await channel.send(f"<:cs_stop:665173353874587678> {member.mention} - 서버 정책에 따라, 생성된 지 3일이 되지 않은 계정은 추방 처리됩니다!\n당신의 계정은 만든지 {text} 정도 지나고 있습니다. 나중에 다시 방문해주세요!")
                await asyncio.sleep(3)
                await member.kick(reason="계정이 활동한 기간이 너무 짧습니다!")

    @commands.command(name="재시작")
    @commands.is_owner()
    async def _reload(self, ctx, *, module):
        try:
            self.SMT.reload_extension(f"{module}")
            await ctx.message.add_reaction("<:cs_reboot:659355468791283723>")
        except Exception as error:
            await ctx.send(f"<:cs_protect:659355468891947008> {ctx.author.mention} - 가끔은 문제가 생길 수도 있는 거지. 자, 여기!\n```{error}```")

    @commands.command(name="해봐", aliases=["실행", "eval", '에뮬'])
    @commands.is_owner()
    async def _evaluate(self, ctx, *, cmd):
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        insert_returns(body)

        env = {
            'SMT': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__,
            'asyncio': asyncio,
            'datetime': datetime,
            'aiohttp': aiohttp,
            'os': os,
        }
        try:
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))    
        except Exception as error:
            await ctx.send(f"<:cs_protect:659355468891947008> {ctx.author.mention} - 가끔은 문제가 생길 수도 있는 거지. 자, 여기!\n```{error}```")
        else:
            if result is not None:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} - 다 됐어! 더 하고 싶은 거 있어?\n```{result}```")
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} - 다 됐어! 더 하고 싶은 거 있어?")

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