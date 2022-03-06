import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from plantnet import plantnet_id

# environment variables for test server
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None, activity = discord.Game(name="!help id"))      # character used to invoke bot commands

# confirmation of bot startup
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.reply("There is a problem processing this image, please try another.") 
        with open('err.log', 'a') as f:
            f.write(f'Time: {datetime.utcnow()}\nCommand Invoke Error: {error}\n\n')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.reply("Did you mean *!id*?")
    else:
        with open('err.log', 'a') as f:
            f.write(f'Time: {datetime.utcnow()}\nUnspecified Error: {error}\n\n')
        await ctx.reply("An error has occured. Please try again.")
        raise error


# ignore non !id commands
@bot.event
async def on_message(message):
    if message.content == '!help id':                                                           # invoke plant id help
        await bot.process_commands(message)
    elif message.content.lower().startswith('!id'):                                             # invoke plant id
        await bot.process_commands(message)


# PLANT ID command listener
@bot.command(name='id')
async def start_id(ctx, *args):

    if len(ctx.message.attachments) > 5:
        await ctx.reply("Please attach up to 5 photos max.")
    elif ctx.message.attachments:
        image_paths = []
        for attachment in ctx.message.attachments:
            image_paths.append(attachment.url)
        response = plantnet_id(image_paths, *args)
        
        # message results
        alternatives_list =[]                                                                   # a list for all the alternative plant IDs

        for result in response[1:]:
            score = format(result['Score'] * 100, ".0f")
            if int(score) >= 10:                                                                # only add alternatives if the confidence score is > 10%
                alternatives_list.append(result['Scientific Name'] + " (" + score + "%)")

        common_names_str =  ", ".join(str(elem) for elem in response[0]['Common Names'])        # convert list to string
        alternatives_str = ", ".join(str(elem) for elem in alternatives_list)                   # convert list to string

        # await ctx.reply(f"My best guess is ***{response[0]['Scientific Name']}*** with {response[0]['Score']*100:.0f}% confidence. Common names include **{common_names_str}**. For more information visit <https://www.gbif.org/species/{response[0]['GBIF']}>\n\nAlternatives include: *{response[1]['Scientific Name']} ({response[1]['Score']*100:.0f}%), {response[2]['Scientific Name']} ({response[2]['Score']*100:.0f}%)*")

        await ctx.reply(f"My best guess is ***{response[0]['Scientific Name']}*** with {response[0]['Score']*100:.0f}% confidence. Common names include **{common_names_str}**. For more information visit <https://www.gbif.org/species/{response[0]['GBIF']}>\n\nAlternatives include: *{alternatives_str}*")
    else:
        await ctx.reply("Attach at least one photo to ID.")


# plant ID help
@bot.command(name='help')
async def help_id(ctx, *args):
    await ctx.message.add_reaction(emoji = '\N{THUMBS UP SIGN}')
 
    embed = discord.Embed(title="Let's break this down a bit:", colour=discord.Colour(0x80eef9), description="Attach up to 5 photos to your message, and then use the following syntax: ```\n!id [args...]\n\neg. !id flower leaf leaf```\nAccepted arguments are 'flower', 'leaf', 'fruit', 'bark'.\n\n", timestamp=datetime.utcnow())
    # embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    # embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_author(name="Plant ID Bot Help", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="Powered by Pl@ntNet API", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.add_field(name="For best results:", value="- all photos should be of the same plant\n- take photos of organs, not the whole plant\n- best results will be achieved by using a mixture of organs\n- use images at least 600x600px\n- add an argument per attached photo, in order.\n- note: incorrect or omitted arguments will default to 'flower'\n\n", inline=True)
    await ctx.send(embed=embed)


bot.run(TOKEN)