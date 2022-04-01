import discord
import typing
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions

class Administration(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
    
    @commands.command(name='change-nickname', aliases=['nick'])
    async def change_nickname(self, ctx: discord.ext.commands.Context, *, nickname: str):
        """Change your nickname using this command\n
        Usage: ?change-nickname <nickname> or ?nick <nickname>
        This command is only usable in the channel id: 868881526778118174"""
        if ctx.channel.id == 868881526778118174:
            await ctx.author.edit(nick=nickname)
            emoji = discord.utils.get(self.bot.emojis, name='ekdom_thik')
            await ctx.message.add_reaction(emoji)
            msg = await ctx.reply(f'Nickname changed to {nickname}')
            await asyncio.sleep(3)
            await ctx.message.delete()
            await msg.delete()

    @commands.command(name='clear-nickname', aliases=['clr-nick'])
    async def clear_nickname(self, ctx: discord.ext.commands.Context):
        """Clear your nickname using this command\n
        Usage: ?clear-nickname or ?clear-nickname"""
        if ctx.channel.id == 868881526778118174:
            await ctx.author.edit(nick=None)
            emoji = discord.utils.get(self.bot.emojis, name='ekdom_thik')
            await ctx.message.add_reaction(emoji)
            msg = await ctx.reply('Nickname cleared')
            await asyncio.sleep(3)
            await ctx.message.delete()
            await msg.delete()

    @commands.command(name='delete', aliases=['purge'])
    @has_permissions(manage_messages=True)
    async def delete_command(self, ctx: discord.ext.commands.Context, amount: int, force: typing.Optional[str]):
        """Delete messages using this command\n
        Usage: ?delete <amount> or ?purge <amount>
        To force to delete messages(slowly), use ?delete <amount> force or ?delete <amount> force"""
        if force == 'force':
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'{amount} messages deleted')                

        else:
            if amount > 120:
                await ctx.send('You can only delete 120 messages at a time')
            else:
                await ctx.channel.purge(limit=amount)
                await ctx.send(f'{amount} messages deleted')
    
    @delete_command.error
    async def delete_command_error(self, ctx: discord.ext.commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the amount of messages to delete')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply('You do not have permission to use this command')
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply('You do not have permission to use this command')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Please specify the amount of messages to delete')
        else:
            pass

    @commands.command(name='dlt')
    async def delete_command_all_users(self, ctx: discord.ext.commands.Context, amount: int, *, force: typing.Optional[str]):
        """Delete your messages using this command\n
        Usage: ?dlt <amount> or ?dlt <amount> force
        To force to delete messages(slowly), use ?dlt <amount> force or ?dlt <amount> force"""
        if force == 'force':
            await ctx.channel.purge(limit=amount, check=lambda m: m.author == ctx.author)
            await ctx.send(f'{amount} messages deleted')               

        else:
            if amount > 120:
                await ctx.send('You can only delete 120 messages at a time')
            else:
                await ctx.channel.purge(limit=amount, check=lambda m: m.author == ctx.author)
                await ctx.send(f'{amount} messages deleted')

    @delete_command_all_users.error
    async def delete_command_all_users_error(self, ctx: discord.ext.commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the amount of messages to delete')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply('You do not have permission to delete messages')
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply('You can only delete your own messages')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Please specify the amount of messages to delete')
        else:
            pass

    @commands.command(name='kick')
    @has_permissions(kick_members=True)
    async def kick_command(self, ctx: discord.ext.commands.Context, member: discord.Member, *, reason: typing.Optional[str]):
        """Kick a member using this command\n
        Usage: ?kick <member> <reason> or ?kick <member>"""
        if reason is None:
            await member.kick()
        else:
            await member.kick(reason=reason)
        await ctx.send(f'{member} was kicked')

    @kick_command.error
    async def kick_command_error(self, ctx: discord.ext.commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permission to use this command')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Please specify a valid member')
        else:
            pass

    @commands.command(name='ban')
    @has_permissions(ban_members=True)
    async def ban_command(self, ctx: discord.ext.commands.Context, member: discord.Member, *, reason: typing.Optional[str]):
        """Ban a member using this command\n
        Usage: ?ban <member> <reason> or ?ban <member>"""
        await member.ban(reason=reason)
        await ctx.send(f'{member} was banned')

    @ban_command.error
    async def ban_command_error(self, ctx: discord.ext.commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permission to use this command')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Please specify a valid member')
        else:
            pass

def setup(bot):
    bot.add_cog(Administration(bot))