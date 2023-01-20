from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog, slash_command


class BotInfoSlash(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()
        self.prefix = '/'

    # bot info
    @slash_command(description="Displays info and more commands")
    async def info(self, ctx):
        """Sends a help message"""
        info = await self.bot.application_info()
        embed = Embed(
            title='Plant ID Bot Info',
            description=f'{info.description}',
            colour=0x41c03f
        ).add_field(
            name=f'`{self.prefix}info`',
            value='Shows this message',
            inline=True
        ).add_field(
            name=f'`{self.prefix}help`',
            value='Gives detailed help on the plant ID bot',
            inline=True 
        ).add_field(
            name=f'`{self.prefix}stats`',
            value='Bot stats',
            inline=True
        ).add_field(
            name=f'`{self.prefix}invite`',
            value='Bot invite link',
            inline=True
        ).add_field(
            name=f'`{self.prefix}source`',
            value='Links to the bot\'s code repo',
            inline=True
        ).set_footer(text=f'Made by {info.owner}')
        await ctx.respond(embed=embed)

    # bot stats
    @slash_command(description="Displays bot stats")
    async def stats(self, ctx):
        info = await self.bot.application_info()
        embed = Embed(
            title=f'{info.name}',
            description="Stats etc.",
            colour=0x1aaae5,
        ).add_field(
            name='Server Count',
            value=len(self.bot.guilds),
            inline=True
        ).add_field(
            name='User Count',
            value=len(self.bot.users),
            inline=True
        ).add_field(
            name='Uptime',
            value=f'{datetime.now() - self.start_time}',
            inline=True
        ).add_field(
            name='Latency',
            value=f'{round(self.bot.latency * 1000, 2)}ms',
            inline=True
        ).set_footer(text=f'Made by {info.owner}')
        await ctx.respond(embed=embed)

    # Sends the link to the bot's GitHub repo
    @slash_command(description="A link to the bot's source code repository")
    async def source(self, ctx):
        url = 'https://github.com/TheRealOwenRees/plantID_discordbot'
        await ctx.respond(f'View source code and report issues at:\n\n{url}')

    # Sends a bot invite link
    @slash_command(description="Display a bot invite link")
    async def invite(self, ctx):
        url = 'https://discord.com/api/oauth2/authorize?client_id=948227126094598204&permissions=19520&scope=bot'
        await ctx.respond(f'Invite the bot to your server:\n\n[Click here]({url})')

    # list servers that the bot has been invited to
    @slash_command(description="All servers that this bot belongs to")
    async def servers(self, ctx):
        servers = list(self.bot.guilds)
        serverWording = 'servers' if len(servers) > 1 else 'server'
        embed = Embed(
            title=f'Connected on {len(servers)} {serverWording}:',
            description='\n'.join(guild.name for guild in self.bot.guilds),
            colour=0x1aaae5
        )
        await ctx.respond(embed=embed)