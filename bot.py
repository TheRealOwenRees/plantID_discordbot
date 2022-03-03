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


# terminal confirmation of bot startup
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
    else:
        with open('err.log', 'a') as f:
            f.write(f'Time: {datetime.datetime.utcnow()}\nUnspecified Error: {error}\n\n')
        await ctx.reply("An error has occured. Please try again.")
        raise error


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
        
        await ctx.reply(f"My best guess is ***{response[0]['Scientific Name']}*** with {round(response[0]['Score']*100, 2)}% confidence. Common names include **{common_names_str}**. For more information visit <https://www.gbif.org/species/{response[0]['GBIF']}>\n\nAlternatives include:\n*{response[1]['Scientific Name']} ({round(response[1]['Score']*100, 2)}%)\n{response[2]['Scientific Name']} ({round(response[2]['Score']*100, 2)}%)*")

        # embed results
        # embed = discord.Embed(title="Here are the top 3 results:", colour=discord.Colour(0xa08bad), timestamp=datetime.datetime.utcnow())
        # embed.set_thumbnail(url=image_paths[0])
        # embed.set_author(name=bot.user, icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        # embed.set_footer(text="Powered by Pl@ntNet", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        # for result in response:
        #     common_names_str = ", ".join(str(elem) for elem in result['Common Names'])
        #     embed.add_field(name="Name", value=result['Scientific Name'])
        #     embed.add_field(name="Genus", value=result['Genus'])
        #     embed.add_field(name="Family", value=result['Family'])
        #     embed.add_field(name="Common Names", value=common_names_str)
        #     embed.add_field(name="Links", value="https://www.gbif.org/species/"+result['GBIF'])
        #     embed.add_field(name = "Confidence %", value = round(result['Score']*100, 2))
        #     embed.add_field(name = chr(173), value = chr(173))
        #     embed.add_field(name = chr(173), value = chr(173))
        #     embed.add_field(name = chr(173), value = chr(173))

        # await ctx.reply(embed=embed)
    else:
        await ctx.reply("Attach at least one photo to ID.")


bot.run(TOKEN)