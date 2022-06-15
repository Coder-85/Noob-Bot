import discord
import os
import typing
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, has_role
from aiohttp import ClientSession
from contextlib import redirect_stdout
from io import StringIO
import textwrap
import importlib

NOT_FOUND_TEXT = "Invalid query! \
If your query is in any module please tell the author to install the module so that \
you can get the documentation."

SHELL_COMMAND = "pandoc -s -f rst -t plain --wrap=preserve temp.rst -o temp.txt"

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
    async def pydoc(self, ctx, *, name: str):
        """Get documentation for a Python module, function or class\n
        Usage: `?py-doc <your-query>`\n"""

        doc = StringIO()
        with redirect_stdout(doc):
            try:
                help(name)
            except ImportError or ModuleNotFoundError or NameError:
                return await ctx.reply(NOT_FOUND_TEXT)
        
        with open('./temp.rst', 'w') as f:
            f.write(doc.getvalue())
        returnCode = os.system(SHELL_COMMAND)
        if returnCode != 0:
            return await ctx.reply("Failed to generate documentation!")

        with open('./temp.txt', 'r') as f:
            content = f.read()
        
        os.system("rm temp.rst")
        os.system("rm temp.txt")
        if content.startswith("No Python documentation found for"):
            return await ctx.reply(NOT_FOUND_TEXT)

        info = content[content.find('\n'):].strip().replace(' |  ', '')
        title = info[:info.find('\n')]

        summary = ''
        for line in info.strip().replace(title, '').split('\n'):
            if len(summary) < 1021:
                summary += line + '\n'
            else:
                summary += '...'
                break

        embed = discord.Embed(title=discord.utils.escape_markdown(title), 
            description=discord.utils.escape_markdown(summary),
            colour=discord.Colour.random()
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GetDocumentation(bot))
