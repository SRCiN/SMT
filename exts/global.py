import discord
from discord.ext import commands
import aiosqlite
import locale
locale.setlocale(locale.LC_ALL, '')

class Global(commands.Cog, name="범용"):
    def __init__(self, SMT):
        self.SMT = SMT

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

def setup(SMT):
    SMT.add_cog(Global(SMT))
