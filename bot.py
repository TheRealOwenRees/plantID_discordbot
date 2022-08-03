import os
import asyncio

from dotenv import load_dotenv

import discord
from discord.ext import commands

from cogs.plantnet_id import PlantnetID
from cogs.bot_info import BotInfo

# environment variables for test server
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

async def main():
    prefix = os.environ.get('BOT_PREFIX', '!')
    bot = commands.Bot(
        command_prefix=prefix, 
        case_insensitive=True, 
        help_command=None,
        activity=discord.Game(name=f'Plants | {prefix}idhelp')
    )
    bot.add_cog(PlantnetID(bot))
    bot.add_cog(BotInfo(bot))

    # confirmation of bot startup
    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.close()