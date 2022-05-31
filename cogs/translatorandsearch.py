import discord
import os
import typing
import asyncio
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, has_role
from googletrans import Translator, LANGUAGES

class TranslateAndSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def getLangName(lang: str):
        for name, code in LANGUAGES.items():
            if code == lang:
                return name
        return lang

    @staticmethod
    def lcs(strning1: str, string2: str):
        m = len(strning1)
        n = len(string2)
        counter = [[0] * (n + 1) for x in range(m + 1)]
        longest = 0
        for i in range(m):
            for j in range(n):
                if strning1[i] == string2[j]:
                    c = counter[i][j] + 1
                    counter[i + 1][j + 1] = c
                    if c > longest:
                        longest = c
        return {
            'longest': longest,
            'for': strning1
        }

    @staticmethod
    def getClosestLang(lang: str):
        if len(lang) <= 2:
            return "Invalid Language Code!" 

        else:
            lcs = 0
            common = ""
            for name in LANGUAGES.values():
                if TranslateAndSearch.lcs(name, lang)['longest'] > lcs:
                    common = TranslateAndSearch.lcs(name, lang)['for']
                    lcs = TranslateAndSearch.lcs(name, lang)['longest']

            return f"Invalid Language! Maybe you meant: **{common.lower()}**?"


    @commands.command(name='translate', aliases=['tto'])
    async def translate(self, ctx, *, text: str):
        """Translates text to your desired language\n
        Usage: `?translate <language> <text>` or `?tto <language> <text>`\n"""
        translator = Translator()
        langtoTranslate = text.split(' ')[0].lower()
        text = ' '.join(text.split(' ')[1:])
        if langtoTranslate in LANGUAGES.items():
            langtoTranslate = TranslateAndSearch.getLangName(langtoTranslate.lower())

        if langtoTranslate not in LANGUAGES.values() and langtoTranslate not in LANGUAGES.keys():
            return await ctx.reply(TranslateAndSearch.getClosestLang(langtoTranslate))
        
        try:
            translation = translator.translate(text, dest=langtoTranslate)
        except:
            return await ctx.reply("Failed to translate :(")

        embed = discord.Embed(
            title=f"Translated from {LANGUAGES[translation.src]} to {LANGUAGES[translation.dest]}", 
            description=translation.text,
            colour = discord.Colour.random()
            )

        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command(name='search', aliases=['google'])
    async def search(self, ctx, *, text: str):
        """Searches for text on Google\n
        Usage: `?search <text>` or `?google <text>`\n"""

        url = f"https://www.google.com/search?q={text.replace(' ', '+')}"
        embed = discord.Embed(
            title=f"Results for **{text}**",
            url=url,
            colour = discord.Colour.random()
        )

        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command(name='search-r', aliases=['google-r'])
    async def searchWithResults(self, ctx, *, text: str):
        """Searches for text on Google and send top 6 results\n
        Usage: `?search-r <text>` or `?google-r <text>` \n"""
    
        url = f"https://www.google.com/search?q={text.replace(' ', '+')}"
        embed = discord.Embed(
            title=f"Results for **{text}**",
            url=url,
            colour = discord.Colour.random()
        )
        
        with ctx.typing():
            r = requests.get(f"https://www.googleapis.com/customsearch/v1?key={os.getenv('GOOGLE_API_KEY')}&cx={os.getenv('CX_TOKEN')}&q={text}").json()
            index = 1
            for i in r.get('items', None):
                if i.get('kind', None) == 'customsearch#result':
                    try:
                        embed.add_field(name=f"Result: {index}", value=f"**[{i['title']}]({i['link']})** \n{i['snippet']}", inline=False)
                        index += 1
                    except:
                        pass

                if index > 6: break

            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(TranslateAndSearch(bot))