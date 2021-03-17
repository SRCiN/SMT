import discord
from discord.ext import commands
import aiosqlite
import asyncio

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
            await o.close()

def setup(SMT):
    SMT.add_cog(Commmands(SMT))
