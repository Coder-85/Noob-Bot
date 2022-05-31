import discord
import typing
import asyncio
import aiohttp
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, has_role
import re
from .helpers import runcode

class CodeRunner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='exec', aliases=['r', 'run', 'eval', 'e'])
    async def exec(self, ctx, *, code: str):
        """Executes a code snippet in the Python 3 environment"""
        result = runcode.post_eval_req(code)

        await ctx.reply(result)

def setup(bot):
    bot.add_cog(CodeRunner(bot))