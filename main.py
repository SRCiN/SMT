import discord
from discord.ext import commands
import config

SMT = commands.Bot(command_prefix=commands.when_mentioned, description="관리를 하는 쉬운 방법", fetch_offline_members=True, intents=discord.Intents.all())
SMT.remove_command('help')
m = ['exts.global', 'exts.cmds', "jishaku", "exts.miya", "exts.events", "exts.health"]

for module in m:
    try:
        SMT.load_extension(module)
    except:
        print(module)

SMT.run(config.Token)
