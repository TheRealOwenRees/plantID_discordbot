import os
import asyncio
import logging

from dotenv import load_dotenv

import discord
from discord.ext import commands

from cogs.plantnet_id import PlantnetID
from cogs.bot_info import BotInfo

load_dotenv()   # load environment variables for test server
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('discord')
logger.setLevel(logging.CRITICAL)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

prefix = os.environ.get('BOT_PREFIX', '!')
bot = commands.Bot(
    command_prefix=prefix, 
    case_insensitive=True, 
    help_command=None,
    activity=discord.Game(name=f'Guess the Plant | {prefix}idhelp')
)
bot.add_cog(PlantnetID(bot))
bot.add_cog(BotInfo(bot))

# confirmation of bot startup
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(DISCORD_TOKEN)