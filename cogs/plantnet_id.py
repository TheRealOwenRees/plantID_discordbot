import os
from discord import ApplicationContext, Embed, Colour, Attachment, option, File
from discord.ext.commands import Cog, BucketType, slash_command, cooldown
from dotenv import load_dotenv
from processing import process_response

load_dotenv()  # load environment variables for test server
API_KEY = os.getenv('PLANTNET_API_KEY')
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"


class PlantnetID(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = '/'

    # help menu
    @slash_command(description="Display the help menu")
    async def help(self, ctx):
        embed = Embed(title="Let's break this down a bit:", colour=Colour(0x80eef9),
                      description="Use the `/id` command and add up to 5 photos\n\n")
        embed.set_author(name="Plant ID Bot Help", url="https://discordapp.com",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text="Powered by Pl@ntNet API", icon_url="https://www.iona.edu/sites/default/files/2021-04"
                                                                  "/ancillary-images/green-flower.jpg")
        embed.add_field(name="For best results:",
                        value="- all photos should be of the same plant\n- take photos of organs, not the whole "
                              "plant\n"
                              "- best results will be achieved by using a mixture of organs\n- use images at least "
                              "600x600px\n\n",
                        inline=True)
        embed.add_field(name=f"`{self.prefix}info`",
                        value="for more commands")
        await ctx.respond(embed=embed)

    # ID from photos
    @slash_command(description="ID a plant from up to 5 photos")
    @cooldown(20, 86400, BucketType.user)  # ENABLE IN PRODUCTION
    @option("image1", Attachment, description="a photo", required=True)
    @option("image2", Attachment, description="a photo", required=False)
    @option("image3", Attachment, description="a photo", required=False)
    @option("image4", Attachment, description="a photo", required=False)
    @option("image5", Attachment, description="a photo", required=False)
    async def id(
            self,
            ctx: ApplicationContext,
            image1: Attachment, image2: Attachment, image3: Attachment,
            image4: Attachment, image5: Attachment,
    ):
        try:
            await ctx.defer()
            attachments = [image1, image2, image3, image4, image5]
            image_paths = [attachments.url for attachments in attachments if attachments is not None]
            images_message = "\n".join([f"[Original Image]({url})" for url in image_paths if url is not None])
            id_result = process_response(image_paths)
            combined_message = id_result + "\n\n" + images_message
            await ctx.respond(combined_message)  # change to ctx.followup.send?

        except Exception as e:
            print(e)
            await ctx.respond(
                'There was a problem processing this image. Either the image format is incorrect or the API is '
                'currently down.')
