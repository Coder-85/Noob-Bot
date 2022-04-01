import discord
import typing
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, has_role

class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='emoji')
    async def emoji_command(self, ctx: discord.ext.commands.Context, emoji: str):
        """Get the emoji's url\n
        Usage: ?emoji <emoji>"""
        emoji = discord.utils.get(self.bot.emojis, name=emoji)
        await ctx.reply(f'{emoji}')

    @emoji_command.error
    async def emoji_command_error(self, ctx: discord.ext.commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the emoji')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Please specify the emoji')
        else:
            pass

    @commands.command(name='react')
    async def react_command(self, ctx: discord.ext.commands.Context, emoji):
        """React the given emoji to the referenced message\n
        Usage: ?react <emoji> to a replied message"""
        emoji = discord.utils.get(self.bot.emojis, name = str(emoji))
        emoji_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if emoji_message is None:
            return await ctx.reply('Could not find the message')

        await emoji_message.add_reaction(emoji)
        try:
            await ctx.delete()
        except:
            pass
        await asyncio.sleep(5)
        await emoji_message.remove_reaction(emoji, self.bot.user)

    @react_command.error
    async def react_command_error(self, ctx: discord.ext.commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the emoji')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Please specify the emoji')
        else:
            pass

def setup(bot):
    bot.add_cog(Emoji(bot))