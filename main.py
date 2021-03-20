import locale

import config
import discord
from discord.ext import commands
from discord_slash import SlashCommand

locale.setlocale(locale.LC_ALL, "")

SMT = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="Shark1ight Moderation Tools",
    help_command=None,
    chunk_guilds_at_startup=True,
    intents=discord.Intents.all(),
)
slash = SlashCommand(SMT, sync_commands=True)
m = [
    "exts.global", "exts.cmds", "jishaku", "exts.miya", "exts.events",
    "exts.health"
]

for module in m:
    try:
        SMT.load_extension(module)
    except:
        print(module)

SMT.run(config.Token)
