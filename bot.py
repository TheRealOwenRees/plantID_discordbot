import os
import logging
from dotenv import load_dotenv 
import discord
from discord.ext import commands

from cogs.plantnet_id_slash import PlantnetIDSlash
from cogs.bot_info_slash import BotInfoSlash
from cogs.plantnet_id import PlantnetID
from cogs.bot_info import BotInfo

load_dotenv()   # load environment variables for test server
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('discord')
# logger.setLevel(logging.CRITICAL)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

# COMMENT OUT INTENTS IN PRODUCTION IF MESSAGES DONT DELIVER
intents = discord.Intents.default()
intents.message_content = True

prefix = os.environ.get('BOT_PREFIX', '!')
bot = commands.Bot(
    command_prefix=prefix, 
    case_insensitive=True, 
    intents=intents,            # COMMENT OUT IN PRODUCTION IF MESSAGES DONT DELIVER
    help_command=None,
    activity=discord.Game(name=f'Guess the Plant | {prefix}idhelp')
)
bot.add_cog(BotInfoSlash(bot))
bot.add_cog(PlantnetIDSlash(bot))
bot.add_cog(PlantnetID(bot))
bot.add_cog(BotInfo(bot))


# convert seconds into hours/minutes/seconds
def convert_seconds(s):
    minute, sec = divmod(s, 60)
    hour, minute = divmod(minute, 60)
    return "%dh %0dm %0ds" % (hour, minute, sec)


# cooldown message
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You have reached the maximum requests allowed in 24h.\nPlease try again in {convert_seconds(error.retry_after)}, or consider using the PlantNet app that this bot is based on.')


# confirmation of bot startup
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(DISCORD_TOKEN)
