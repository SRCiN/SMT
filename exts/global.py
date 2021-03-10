import discord
from discord.ext import commands
import datetime
import aiohttp
import os
import asyncio

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
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
                await ctx.send(f":mag_right: {ctx.author.mention} - `{error.argument}`(이)라는 값과 관련된 유저를 발견하지 못했습니다.")
            elif isinstance(error, commands.ChannelNotFound):
                await ctx.send(f":mag_right: {ctx.author.mention} - `{error.argument}`(이)라는 값과 관련된 채널을 발견하지 못했습니다.")
            elif isinstance(error, commands.ChannelNotReadable):
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - `{error.argument}`(이)라는 값과 관련된 유저를 발견하지 못했습니다.")
            elif isinstance(error, commands.RoleNotFound):
                await ctx.send(f":mag_right: {ctx.author.mention} - `{error.argument}`(이)라는 값과 관련된 유저를 발견하지 못했습니다.")
            else:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 지급된 값이 잘못되었습니다. 명령어 사용법을 확인해주세요.")
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 이 명령어는 사용 권한이 제한됩니다. 관리자에게 문의하세요.")
        elif isinstance(error, commands.MissingAnyRole) or isinstance(commands.MissingRole):
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 이 명령어를 사용하려면 특정한 역할이 필요합니다.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f":stopwatch: {ctx.author.mention} - 명령어 재사용 대기 시간입니다.{round(error.retry_after, 2)}초 후에 다시 시도하세요.")
        else:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 예기치 못한 오류로 인해 실행할 수 없었습니다. 관리자에게 문의하세요.")
            channel = self.SMT.get_channel(783621627875164230)
            await channel.send(f'도와주고 있는데, 문제가 좀 생긴 것 같아. 네가 확인해줄래? ```{error}```')

def setup(SMT):
    SMT.add_cog(Global(SMT))
