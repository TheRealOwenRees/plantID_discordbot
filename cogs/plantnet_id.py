import os
from dotenv import load_dotenv
from processing import process_attachments

import discord
from discord.ext.commands import Cog, command, cooldown, BucketType

load_dotenv()  # load environment variables for test server
API_KEY = os.getenv('PLANTNET_API_KEY')
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"


class PlantnetID(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = '!'
        if 'BOT_PREFIX' in os.environ:
            self.prefix = os.environ['BOT_PREFIX']

    # PLANT ID HELP command listener
    @command(aliases=['helpid'])
    async def idhelp(self, ctx):
        await ctx.message.add_reaction(emoji='\N{THUMBS UP SIGN}')
        embed = discord.Embed(title="Let's break this down a bit:", colour=discord.Colour(0x80eef9),
                              description="Attach up to 5 photos to your message and type `!id` as the message\n\n")
        # embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
        # embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_author(name="Plant ID Bot Help", url="https://discordapp.com",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text="Powered by Pl@ntNet API", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="For best results:",
                        value="- all photos should be of the same plant\n- take photos of organs, not the whole "
                              "plant\n-"
                              "best results will be achieved by using a mixture of organs\n- use images at least "
                              "600x600px\n- add an argument per attached photo, in order.\n\n",
                        inline=True)
        embed.add_field(name=f"`{self.prefix}info`",
                        value="for more commands")
        await ctx.send(embed=embed)

    # PLANT ID command listener
    @command()
    @cooldown(20, 86400, BucketType.user)  # ENABLE IN PRODUCTION
    async def id(self, ctx):
        try:
            # prevent more than 5 photos from being processed (Plantnet max)
            if len(ctx.message.attachments) > 5:
                await ctx.reply("Please attach up to 5 photos max.")
            # process images
            elif ctx.message.attachments:
                image_paths = []
                for attachment in ctx.message.attachments:
                    image_paths.append(attachment.url)
                await ctx.reply(process_attachments(image_paths))
            # process url instead of image
            elif len(ctx.message.attachments) == 0 and len(ctx.message.content) > 3:
                image_paths = []  # made into an array for when i expand this to accept multiple urls
                url_text = ctx.message.content[4:]  # only accepts 1 url for now
                image_paths.append(url_text)
                await ctx.reply(process_attachments(image_paths))
            # no attachments or url
            else:
                await ctx.reply("Attach at least one photo to ID.")

        except Exception as e:
            print(e)
            await ctx.send(
                'There was a problem processing this image. Either the image format is incorrect or the API is '
                'currently down.')
