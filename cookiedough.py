import logging
import sys
from discord.ext import commands

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S')

description = '''A cookie loving Discord bot'''
bot = commands.Bot(command_prefix='.', description=description, case_insensitive=True)

# Currently, Database must be loaded FIRST as other cogs that use it will get it during their initialization routines.
bot.load_extension("cogs.database")
bot.load_extension("cogs.economy")
bot.load_extension("cogs.admin")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.main")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.pinboard")
bot.load_extension("cogs.stickers")
bot.load_extension("cogs.testing")

bot.run(sys.argv[1])
