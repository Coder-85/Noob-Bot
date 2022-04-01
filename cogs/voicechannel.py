import discord
import typing
import asyncio
from discord.ext import commands

class VoiceStuff(commands.Cog):
    inserter: discord.Member = None

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="join")
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Joins a voice channel"""
        if channel is None:
            try:
                channel = ctx.author.voice.channel
                await channel.connect()
                return await ctx.reply(f"Connected to <#{channel.id}>")
            except AttributeError:
                return await ctx.send("You are not in a voice channel")
        else:
            try:
                await channel.connect()
                return await ctx.reply(f"Connected to <#{channel.id}>")
            except discord.ClientException:
                return await ctx.send("Already connected to a voice channel")
            except discord.InvalidArgument:
                return await ctx.send("This is not a voice channel")

    @commands.command(name="leave")
    async def leave(self, ctx):
        """Leaves the voice channel"""
        if ctx.voice_client is None:
            return await ctx.send("Not connected to any voice channel")
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel")

def setup(bot):
    bot.add_cog(VoiceStuff(bot))