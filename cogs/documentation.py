import discord
import typing
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, has_role
from aiohttp import ClientSession
from contextlib import redirect_stdout
from io import StringIO
import textwrap
import importlib

class GetDocumentation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pypi', aliases=['pypi-search', 'pip-pkg', 'python-pkg'])
    async def pypi(self, ctx, *, package: str):
        """Search for a package on PyPi\n
        Usage: `?pypi <package-name>`\n"""
        
        embed = discord.Embed()
        session = ClientSession()
        async with session.get(f"https://pypi.org/pypi/{package.lower()}/json") as response:
            if response.status == 404:
                response.close()
                await session.close()
                return await ctx.reply("Package could not be found!")

            data = await response.json()
            info = data['info']

            embed.title = info['name'] + ' v' + info['version']
            embed.url = info['package_url']
            embed.colour = discord.Colour.random()

            summary = discord.utils.escape_markdown(info['summary'])
            if not summary or summary.isspace():
                summary = "No summary provided."

            embed.description = summary

            response.close()
            await session.close()

        await ctx.send(embed=embed)

    @commands.command(name='py-doc', aliases=['python-doc', 'python-docs', 'py-docs', 'pydoc'])
    async def pydocs(self, ctx, *, name: str):
        """Get documentation for a Python module, function or class\n
        Usage: `?py-doc <your-query>`\n"""

        doc = StringIO()
        with redirect_stdout(doc):
            try:
                help(name)
            except:
                try:
                    importlib.import_module(name.split('.', maxsplit=2)[0])
                except ImportError or ModuleNotFoundError or NameError:
                    return await ctx.reply("Query could not be found! \
If your query is in any module please tell the author to install the module so that \
you can get the documentation.")
        
        info = doc.getvalue()[doc.getvalue().find('\n\n'):].strip().replace(' |  ', '')
        title = info[:info.find('\n')]
        if info == '' or title == '':
            return await ctx.reply("Query could not be found! \
If your query is in any module please tell the author to install the module so that \
you can get the documentation.")
        summary = ''
        for line in info[:info.find('Method')].strip().replace(title, '').split('\n'):
            if len(summary) < 1024:
                summary += line + '\n'
            else:
                summary += '...'
                break

        embed = discord.Embed(title=discord.utils.escape_markdown(title), 
            description=discord.utils.escape_markdown(summary), 
            colour=discord.Colour.random()
            )

        if info.find('Method') != -1 and len(info) < 1000:
            methods = info[info.find('Method'):].strip()
            embed.add_field(name='Methods', value=discord.utils.escape_markdown(methods), inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GetDocumentation(bot))