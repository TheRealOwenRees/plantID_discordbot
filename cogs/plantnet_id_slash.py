import os
from dotenv import load_dotenv

import discord
from discord.ext.commands import Cog, cooldown, BucketType, slash_command

from processing import process_attachments


load_dotenv()  # load environment variables for test server
API_KEY = os.getenv('PLANTNET_API_KEY')
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"


class PlantnetIDSlash(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = '/'

    # help menu
    @slash_command(description="Display the help menu")
    async def help(self, ctx):
        embed = discord.Embed(title="Let's break this down a bit:", colour=discord.Colour(0x80eef9),
                              description="Attach up to 5 photos to your message and type `!id` as the message\n\n")
        # embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
        # embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_author(name="Plant ID Bot Help", url="https://discordapp.com",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text="Powered by Pl@ntNet API", icon_url="https://www.iona.edu/sites/default/files/2021-04/ancillary-images/green-flower.jpg")
        embed.add_field(name="For best results:",
                        value="- all photos should be of the same plant\n- take photos of organs, not the whole plant\n- "
                              "best results will be achieved by using a mixture of organs\n- use images at least "
                              "600x600px\n\n",
                        inline=True)
        embed.add_field(name=f"`{self.prefix}info`",
                        value="for more commands")
        await ctx.respond(embed=embed)

    # ID from photos
    # @slash_command(guild_ids=[1002507312159797318], description="ID a plant from up to 5 photos")
    # @cooldown(20, 86400, BucketType.user)     # ENABLE IN PRODUCTION
    # @discord.option("image1", discord.Attachment, description="a photo", required=True)
    # @discord.option("image2", discord.Attachment, description="a photo", required=False)
    # @discord.option("image3", discord.Attachment, description="a photo", required=False)
    # @discord.option("image4", discord.Attachment, description="a photo", required=False)
    # @discord.option("image5", discord.Attachment, description="a photo", required=False)
    # async def id(
    #     self,
    #     ctx: discord.ApplicationContext,
    #     image1: discord.Attachment,
    #     image2: discord.Attachment,
    #     image3: discord.Attachment,
    #     image4: discord.Attachment,
    #     image5: discord.Attachment,
    # ): 
    #     try:
    #         attachments = [image1, image2, image3, image4, image5]
    #         image_paths = []
    #         for attachment in attachments:
    #             if attachment is not None:
    #                 image_paths.append(attachment.url)
    #         result = process_attachments(image_paths)
    #         await ctx.respond(image_paths)
    #         await ctx.respond('dsd')

    #     except Exception as e:
    #         print(e)
    #         await ctx.respond(
    #             'There was a problem processing this image. Either the image format is incorrect or the API is currently down.')

