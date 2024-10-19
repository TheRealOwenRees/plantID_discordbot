import os

from dotenv import load_dotenv
from discord import Game
from discord.ext.commands import Bot, CommandOnCooldown

from cogs.plantnet_id import PlantnetID
from cogs.bot_info import BotInfo

load_dotenv()  # load environment variables for test server
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot(
    case_insensitive=True,
    help_command=None,
    activity=Game(name=f'Guess the Plant | /help')
)
bot.add_cog(BotInfo(bot))
bot.add_cog(PlantnetID(bot))

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
            f'This server has reached the maximum requests allowed in 24h.\n\nPlease try again in {convert_seconds(error.retry_after)}, or consider using the PlantNet app that this bot is based on.')
    else:
        raise error


# confirmation of bot startup
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_disconnect():
    print(f'{bot.user} has disconnected from Discord!')


bot.run(DISCORD_TOKEN)
