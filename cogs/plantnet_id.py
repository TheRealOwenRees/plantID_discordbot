import requests
from discord import ApplicationContext, Embed, Colour, Attachment, option
from discord.ext.commands import Cog, BucketType, slash_command, cooldown
from processing import process_response
from settings import api_base_url, FILE_SERVER_URL, FILE_SERVER_IMAGES_URL, FILE_SERVER_SECRET_KEY


def get_url(attachment):
    response = requests.post(
        FILE_SERVER_URL,
        headers={
            "url": attachment.url, "Authorization": FILE_SERVER_SECRET_KEY
        })

    if response.status_code != 201:
        return None

    filename = response.json()["filename"]
    return f"{FILE_SERVER_IMAGES_URL}/{filename}"


class PlantnetID(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = '/'

    # API status
    @slash_command(description="Check the status of the PlantNet API")
    async def status(self, ctx):
        response = requests.get(f"{api_base_url}/_status")
        if response.status_code != 200:
            await ctx.respond("The PlantNet API is currently down.")
        else:
            await ctx.respond("The PlantNet API is currently up and running.")

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
    @cooldown(20, 86400, BucketType.guild)  # ENABLE IN PRODUCTION
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
        await ctx.defer()
        attachments = [image1, image2, image3, image4, image5]

        image_paths = [get_url(attachments) for attachments in attachments if attachments is not None]

        # use the original Discord image URLs to display them in the embed, allowing us to delete the processed images from the server
        images_message = "\n".join([f"[Original Image]({url})" for url in attachments if url is not None])

        try:
            id_result = process_response(image_paths)
            combined_message = id_result + "\n\n" + images_message
            await ctx.respond(combined_message)

        except Exception as e:
            print(e)
            await ctx.respond(
                'There was a problem processing this image. Either the image format is incorrect or the API is '
                'currently down.')

        finally:
            # delete the processed images from the server
            for url in image_paths:
                file = url.split("/")[-1]
                requests.delete(f"{FILE_SERVER_URL}/{file}", headers={"Authorization": FILE_SERVER_SECRET_KEY})