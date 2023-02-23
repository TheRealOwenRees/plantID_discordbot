import os
import logging
from dotenv import load_dotenv
from discord import Game
from discord.ext.commands import Bot, CommandOnCooldown

from cogs.plantnet_id_slash import PlantnetIDSlash
from cogs.bot_info_slash import BotInfoSlash

load_dotenv()  # load environment variables for test server
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('discord')
logger.setLevel(logging.CRITICAL)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = Bot(
    case_insensitive=True,
    help_command=None,
    activity=Game(name=f'Guess the Plant | /help')
)
bot.add_cog(BotInfoSlash(bot))
bot.add_cog(PlantnetIDSlash(bot))


# convert seconds into hours/minutes/seconds
def convert_seconds(s):
    minute, sec = divmod(s, 60)
    hour, minute = divmod(minute, 60)
    return "%dh %0dm %0ds" % (hour, minute, sec)


# cooldown message
@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.respond(
            f'You have reached the maximum requests allowed in 24h.\n\nPlease try again in {convert_seconds(error.retry_after)}, or consider using the PlantNet app that this bot is based on.')
    else:
        raise error


# confirmation of bot startup
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


bot.run(DISCORD_TOKEN)
