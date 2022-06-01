#! /usr/bin python3
import discord
from discord.ext import commands
from pathlib import Path
import os

TOKEN = os.getenv('BOT_TOKEN')

class NoobBot(commands.Bot):
    def __init__(self):
        self._cogs = [i.stem for i in Path('.').glob('./cogs/*.py')]
        intents = discord.Intents.all()
        super().__init__(command_prefix='?',
                        description='NoobBot', 
                        intents= intents,
                        help_command=None,
                        owner_id=645232980809482250
                        )

    def run(self):
        for cog in self._cogs:
            self.load_extension(f'cogs.{cog}')
            print(f'Loaded {cog}')

        super().run(TOKEN, reconnect=True)

    async def on_connect(self):
        print('Connected to Discord!')

    async def on_disconnect(self):
        print('Disconnected from Discord')

    async def on_ready(self):
        print(f'That bot {self.user}')
        await self.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name = '?help'))

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("?")(bot, msg)

    async def on_message(self, message):
        if message.author == self.user:
            return

        await self.process_commands(message)

    async def on_member_join(self, member):
        chnl = discord.utils.get(member.guild.channels, name = "just-fokin-talk")
        chnl2 = discord.utils.get(member.guild.channels, name = "bot-query")
        if chnl != None:    
            await chnl.send(f"Welcome to the server {member.mention}")
            await member.send("Welcome to the server!\nHave a good time there")
        if chnl2 != None:
            await chnl2.send(f"Welcome to the server {member.mention}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

        raise error

noobbot = NoobBot()
noobbot.run()
