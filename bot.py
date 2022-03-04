from datetime import datetime
import os
from sys import exc_info
import discord
from discord.ext import commands
from dotenv import load_dotenv
from plantnet import plantnet_id
import datetime

# environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)      # character used to invoke bot commands


# confirmation of bot startup
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name='everything you do'))


# error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.reply("There is a problem processing this image, please try another.") 
        with open('err.log', 'a') as f:
            f.write(f'Time: {datetime.datetime.utcnow()}\nCommand Invoke Error: {error}\n\n')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.reply("Are you having a stroke? Did you mean *!id*?")
    else:
        with open('err.log', 'a') as f:
            f.write(f'Time: {datetime.datetime.utcnow()}\nUnspecified Error: {error}\n\n')
        await ctx.reply("An error has occured. Please try again.")
        raise error


# ignore non !id commands
@bot.event
async def on_message(message):
    if message.content.lower().startswith('!id'):
        await bot.process_commands(message)


# PLANT ID command listener
@bot.command(name='id', help="Runs the Plant ID bot. Type '!help id' for more detailed info.")
async def start_id(ctx, *args):

    if len(ctx.message.attachments) > 5:
        await ctx.reply("Please attach up to 5 photos max.")
    elif ctx.message.attachments:
        image_paths = []
        for attachment in ctx.message.attachments:
            image_paths.append(attachment.url)
        response = plantnet_id(image_paths, *args)
        
        # message results
        common_names_str = ", ".join(str(elem) for elem in response[0]['Common Names'])
        
        await ctx.reply(f"My best guess is ***{response[0]['Scientific Name']}*** with {response[0]['Score']*100:.0f}% confidence. Common names include **{common_names_str}**. For more information visit <https://www.gbif.org/species/{response[0]['GBIF']}>\n\nAlternatives include: *{response[1]['Scientific Name']} ({response[1]['Score']*100:.0f}%), {response[2]['Scientific Name']} ({response[2]['Score']*100:.0f}%)*")
    else:
        await ctx.reply("Attach at least one photo to ID.")


bot.run(TOKEN)