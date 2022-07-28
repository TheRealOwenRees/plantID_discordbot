import asyncio
import os

from dotenv import load_dotenv

import discord
from discord.ext import commands
from cogs.plantnet_id import PlantnetID

# environment variables for test server
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

async def main():
    bot = commands.Bot(
        command_prefix='!', case_insensitive=True, 
        help_command=None,
        activity=discord.Game(name="!help-id")
    )
    bot.add_cog(PlantnetID(bot))

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