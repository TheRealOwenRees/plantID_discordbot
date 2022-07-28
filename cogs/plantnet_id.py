import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

import discord
from discord.ext.commands import Cog, command

load_dotenv()
API_KEY = os.getenv('PLANTNET_API_KEY')
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"


class PlantnetID(Cog):
    def __init__(self, bot):
        self.bot = bot

    # PLANT ID command listener
    @command(name='id')
    async def start_id(self, ctx, *args):
        try:
            if len(ctx.message.attachments) > 5:
                await ctx.reply("Please attach up to 5 photos max.")
            elif ctx.message.attachments:
                image_paths = []
                for attachment in ctx.message.attachments:
                    image_paths.append(attachment.url) 
                response = self.plantnet_response(image_paths, *args)

                # message results
                alternatives_list = []  # a list for all the alternative plant IDs

                for result in response[1:]:
                    score = format(result['Score'] * 100, ".0f")
                    if int(score) >= 10:  # only add alternatives if the confidence score is > 10%
                        alternatives_list.append(result['Scientific Name'] + " (" + score + "%)")

                # alternatives - join list as string if true
                if alternatives_list:
                    alternatives_str = "Alternatives include: " + "*" + ", ".join(
                        str(elem) for elem in alternatives_list) + "*."
                else:
                    alternatives_str = "No alternatives were found."

                # common names - join list as string if true
                if response[0]['Common Names']:
                    common_names_str = "Common names include " + "**" + ", ".join(
                        str(elem) for elem in response[0]['Common Names']) + "**."
                else:
                    common_names_str = "No common names were found."

                # GBIF data - create url to GBIF if id is found
                gbif_str = "<https://www.gbif.org/species/" + response[0]['GBIF'] + ">" if \
                    response[0]['GBIF'] else ""

                # PFAF URL - create url to PFAF if latin name is found
                pfaf_str = "<https://pfaf.org/user/Plant.aspx?LatinName=" + response[0]['Scientific Name'].replace(" ", "+") + ">"

                await ctx.reply(
                    f"My best guess is ***{response[0]['Scientific Name']}*** with {response[0]['Score'] * 100:.0f}% "
                    f"confidence. {common_names_str} For more information visit:\n{pfaf_str}\n\n{gbif_str}\n\n{alternatives_str}")
            
            else:
                await ctx.reply("Attach at least one photo to ID.")

        except Exception as e:
            print(e)
            await ctx.send('There was a problem processing this image. Either the image format is incorrect or the API is currently down.')


    # PLANT ID HELP command listener
    @command(name='help-id')
    async def help_id(self, ctx, *args):
        await ctx.message.add_reaction(emoji='\N{THUMBS UP SIGN}')
        embed = discord.Embed(title="Let's break this down a bit:", colour=discord.Colour(0x80eef9),
                            description="Attach up to 5 photos to your message, and then use the following syntax: "
                                        "```\n!id [args...]\n\neg. !id flower leaf leaf```\nAccepted arguments are "
                                        "'flower', 'leaf', 'fruit', 'bark'.\n\n",
                            timestamp=datetime.utcnow())
        # embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
        # embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_author(name="Plant ID Bot Help", url="https://discordapp.com",
                        icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text="Powered by Pl@ntNet API", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="For best results:",
                        value="- all photos should be of the same plant\n- take photos of organs, not the whole plant\n- "
                            "best results will be achieved by using a mixture of organs\n- use images at least "
                            "600x600px\n- add an argument per attached photo, in order.\n- note: incorrect or omitted "
                            "arguments will default to auto-detect.\n\n",
                        inline=True)
        await ctx.send(embed=embed)


    @staticmethod
    def plantnet_response(images, *organs):

        # a list of accepted organs that can be used as arguments
        accepted_organs = ['flower', 'leaf', 'bark', 'fruit']

        # create dict of params for requests.get()
        payload = {'images':[], 'organs':[]}

        # add params to dict for requests.get()
        for image in images:
            payload['images'].append(image)
        for organ in organs:
            if organ in accepted_organs:
                payload['organs'].append(organ)
            else:
                payload['organs'].append('auto')      # argument default if incorrect or omitted
        
        # send request to API as a url and return as JSON
        req = requests.get(api_endpoint, params=payload)
        if (req.status_code == 200):
            json_data = json.loads(req.text)
        else:
            return False

        # format output
        results_list = []
        
        for result in json_data['results']:
            d= {
                "Score": result['score'],
                "Scientific Name": result['species']['scientificNameWithoutAuthor'],
                "Genus": result['species']['genus']['scientificNameWithoutAuthor'],
                "Family": result['species']['family']['scientificNameWithoutAuthor'],
                "Common Names": result['species']['commonNames'],
                # "GBIF": result['gbif'].get('id')
            }
            d['GBIF'] = result['gbif'].get('id') if result['gbif'] else ""

            results_list.append(d)

        return results_list
