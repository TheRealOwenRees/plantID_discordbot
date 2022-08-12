import os
import requests
import re

from bs4 import BeautifulSoup
from prettytable import PrettyTable, ALL

import discord
from discord.ext.commands import Cog, command


class PfafSearch(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = 'p!'
        if 'BOT_PREFIX' in os.environ:
            self.prefix = os.environ['BOT_PREFIX']
        self.useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:103.0) Gecko/20100101 Firefox/103.0'

    @command(aliases=['s'])
    async def search(self, ctx, *args):
        # initial url to retrieve key form values for aspx scraping
        get_url = requests.get('https://pfaf.org/user/DatabaseSearhResult.aspx')
        soup_dummy = BeautifulSoup(get_url.content, 'html.parser')
        viewstate = soup_dummy.find('input', id='__VIEWSTATE')
        viewstategen = soup_dummy.find('input', id='__VIEWSTATEGENERATOR')

        search_url = 'https://pfaf.org/user/Default.aspx'
        search_params = ' '.join(args)
        print(search_params)
   
        headers = {
            'User-Agent': self.useragent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategen,
            'ctl00$ContentPlaceHolder1$txtSearch': search_params,
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$imgbtnSearch1'
        }

        # parse the result page HTML
        res = requests.post(search_url, headers=headers, data=data)
        soup = BeautifulSoup(res.content, 'html.parser')

        # new ascii table instance
        ascii_table = PrettyTable()
        ascii_table.hrules=ALL

        # find the table that contains the results
        rows = soup.find('table', id='ContentPlaceHolder1_gvresults').find_all('tr')

        # find table headers + add to ascii_table
        th = rows[0].find_all('th')

        ascii_table.field_names = [
            th[0].get_text(),
            th[1].get_text(),
            # th[2].get_text(),
            # th[3].get_text(),
            # th[4].get_text(),
            # th[5].get_text(),
            # th[6].get_text(),
            # th[7].get_text(),
            # th[8].get_text(),
            # th[9].get_text(),
            # th[10].get_text(),
        ]

        for row in rows[1:]:
            content = row.find_all('td')
            latin_name = content[0].get_text()
            common_name = content[1].get_text()
            # habit = content[2].get_text()
            # height = content[3].get_text()
            # hardiness = content[4].get_text()
            # growth = content[5].get_text()
            # soil = content[6].get_text()
            # shade = content[7].get_text()
            # moisture = content[8].get_text()
            # edible = content[9].get_text()
            # medicinal = content[10].get_text()

            ascii_table.add_row([
                latin_name.replace(' ', '\n'), 
                common_name.replace(',', '\n'),
                # habit,
                # height,
                # hardiness,
                # growth,
                # soil,
                # shade,
                # moisture,
                # edible,
                # medicinal,
            ])

        ascii_table_str = ascii_table.get_string()
        print(ascii_table_str)

        await ctx.reply(f'```{ascii_table_str if len(ascii_table_str) <= 2000 else "Your search returned too many results to display. Please narrow your search"}```')

    @command(aliases=['d'])
    async def details(self, ctx, *args):
        details_url = "https://pfaf.org/user/Plant.aspx?LatinName="
        unwanted_args = ["-v", "-V"]
        new_args = [i for i in args if i not in unwanted_args]
        args_str = '+'.join(new_args)
        res = requests.get(f'{details_url}{args_str}', headers={'User-Agent': self.useragent,})
        soup = BeautifulSoup(res.content, 'html.parser')

        async def basic_details(ctx):        
            table_title = soup.find('span', id='ContentPlaceHolder1_lbldisplatinname').text
            rows = soup.find('table', class_='table table-hover table-striped').find_all('tr')

            message_str = f'**{table_title}**\n<{details_url}{args_str}>\n'

            for row in rows[:10]:
                content = row.find_all('td')
                left_text = content[0].get_text().strip()
                right_text = content[1].get_text().strip()
                message_str += f'```{left_text}:\n\t{right_text}\n\n```\n\n'

            # separate 'care info' due to needing to retrieve 'alt' data
            care_info_str = f'{rows[10].find("td").get_text().strip()}:\n'
            care_info_table = rows[10].find('table', id='ContentPlaceHolder1_tblIcons')
            img_row = care_info_table.find_all('img', alt=True)
            for img in img_row:
                care_info_str += f'\t{img.get("alt")}\n'
            care_info_block = f'```{care_info_str}```'

            await ctx.reply(f'Here are the details for: {message_str}{care_info_block}\nRun the command with -v for a more detailed result.')

        async def verbose_details(ctx):
            await basic_details(ctx)

            too_long_str = 'Too long to display here, please visit the PFAF.org link at the top of the first message'

            rsub = r'\[[^\]]*\]'   # regex pattern to remove square brackets and their contents
            rows = soup.find_all('span')
            summary = re.sub(rsub, '', f'```Summary:\n\t{rows[15].get_text() if len(rows[15].get_text()) <= 2000 else too_long_str}```')
            phy_char = re.sub(rsub, '', f'```Physical Characteristics:\n\t{rows[16].get_text() if len(rows[16].get_text()) <= 2000 else too_long_str}```')
            synonyms = re.sub(rsub, '', f'```Synonyms:\n\t{rows[17].get_text() if len(rows[17].get_text()) <= 2000 else too_long_str}```')
            habitats = re.sub(rsub, '', f'```Habitats:\n\t{rows[18].get_text() if len(rows[18].get_text()) <= 2000 else too_long_str}```')
            edible_uses = re.sub(rsub, '', f'```Edible Uses:\n\t{rows[19].get_text() if len(rows[19].get_text()) <= 2000 else too_long_str}```')
            medicinal_uses = re.sub(rsub, '', f'```Medicinal Uses:\n\t{rows[20].get_text() if len(rows[20].get_text()) <= 2000 else too_long_str}```')
            other_uses = re.sub(rsub, '', f'```Other Uses:\n\t{rows[22].get_text() if len(rows[22].get_text()) <= 2000 else too_long_str}```')
            special_uses = re.sub(rsub, '', f'```Special Uses:\n\t{rows[23].get_text() if len(rows[23].get_text()) <= 2000 else too_long_str}```')
            cultivation = re.sub(rsub, '', f'```Cultivation Details:\n\t{rows[24].get_text() if len(rows[24].get_text()) <= 2000 else too_long_str}```')
            propagation = re.sub(rsub, '', f'```Propagation:\n\t{rows[27].get_text() if len(rows[27].get_text()) <= 2000 else too_long_str}```')

            await ctx.reply(f'{summary}\n\n{phy_char}\n\n{synonyms}\n\n{habitats}')
            await ctx.reply(f'{edible_uses}\n\n{medicinal_uses}')
            await ctx.reply(f'{other_uses}\n\n{special_uses}')
            await ctx.reply(f'{cultivation}')
            await ctx.reply(f'{propagation}')

        await verbose_details(ctx) if any(arg.lower() == '-v' for arg in args) else await basic_details(ctx)

