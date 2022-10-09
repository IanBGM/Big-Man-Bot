import random
import re

import nextcord
import requests
from googletrans import Translator
from nextcord.ext import commands
from urllib import parse, request

from External import Colors


class Entertainment(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # @commands.command(aliases=['convert'], usage='translate <language> <message>')
    # async def translate(self, ctx, language: str, *, message: str):
    #     """Translate messages to another language!"""
    #     translator = Translator()
    #
    #     try:
    #         translation = translator.translate(message, dest=language)
    #     except ValueError:
    #         return await ctx.send("Ay.. (Something went wrong.. is that language correct?)")
    #
    #     translateEmbed = nextcord.Embed(title='Ay! (Translation!)', description=f"Ay \n```\n(\"{translation.text}\")\n```", color=Colors.dark_grey, timestamp=ctx.message.created_at)
    #     translateEmbed.set_footer(text=f"Ay! (Language: {language.upper()}!)")
    #
    #     await ctx.send(embed=translateEmbed)

    @commands.command(name='8ball', aliases=['fortune'], usage='8ball <message>')
    async def _8ball(self, ctx, *, message: str):
        """Ask questions! Get answers!"""

        inputs = [
            "Ay.. (I'm not too sure..)",
            "Ay! Ay! Ay! (Yes, Yes, Yes!)",
            "Ay.. Ay.. Ay.. (No, No, No..)"
            "Ay! (For sure!)",
            "Ay.. (I don't think so..)",
            "Ay (No)",
            "Ay (Yes)",
            "Ay..? (I didn't quite catch that..)",
            "Ay- (Uhm-)",
            "Ay? (Maybe?)"
        ]

        _8ballEmbed = nextcord.Embed(title="Ay! (Question Asked!)", color=Colors.dark_grey, timestamp=ctx.message.created_at)

        if message.lower() != "are you real?":
            _8ballEmbed.add_field(name='Ay (Question)', value=f"*`Ay (\"{message}\")`*", inline=False)
            _8ballEmbed.add_field(name='Ay (Answer)', value=f"*`{random.choice(inputs)}`*", inline=False)
        else:
            _8ballEmbed.add_field(name='Ay (Question)', value=f"*`Ay (\"{message}\")`*", inline=False)
            _8ballEmbed.add_field(name='Ay (Answer)', value=f"*`Ay. (Yes. Or am I? This is confusing..)`*", inline=False)

        await ctx.send(embed=_8ballEmbed)

    @commands.command(aliases=['backwards'], usage='reverse <message>')
    async def reverse(self, ctx, *, message: str):
        """Reverse messages to make them backwards!"""

        reverseEmbed = nextcord.Embed(title='Ay! (Reversed!)', description=f"Ay \n```\n(\"{message[::-1]}\")\n```", color=Colors.dark_grey, timestamp=ctx.message.created_at)

        await ctx.send(embed=reverseEmbed)

    # @commands.command(aliases=['yt-search', 'yt'], usage='youtube <message>')
    # async def youtube(self, ctx, *, message: str):
    #     """Search for something on YouTube!"""
    #
    #     query_string = parse.urlencode({'search_query': message})
    #     htm_content = request.urlopen(
    #         'http://www.youtube.com/results?' + query_string)
    #     search_results = re.findall(r'/watch\?v=(.{11})',
    #                                 htm_content.read().decode())
    #     await ctx.send("Ay\n" + 'http://www.youtube.com/watch?v=' + search_results[0])

    @commands.command(usage='cat')
    async def cat(self, ctx):
        """Look at images of cats!"""
        response = requests.get('https://some-random-api.ml/img/cat')
        data = response.json()
        # noinspection PyBroadException
        try:
            catEmbed = nextcord.Embed(title="Ay!? (Cat!?)", color=Colors.dark_grey, timestamp=ctx.message.created_at)
            catEmbed.set_image(url=data['link'])
            return await ctx.send(embed=catEmbed)
        except:
            return await ctx.send("Ay.. (An error has occurred.. maybe try again later..)")

    @commands.command(usage='dog')
    async def dog(self, ctx):
        """Look at images of dogs!"""
        response = requests.get('https://some-random-api.ml/img/dog')
        data = response.json()
        # noinspection PyBroadException
        try:
            dogEmbed = nextcord.Embed(title="Ay!? (Dog!?)", color=Colors.dark_grey, timestamp=ctx.message.created_at)
            dogEmbed.set_image(url=data['link'])
            return await ctx.send(embed=dogEmbed)
        except:
            return await ctx.send("Ay.. (An error has occurred.. maybe try again later..)")

    @commands.command(aliases=['base'], usage='base64 <message>')
    async def base64(self, ctx, *, message: str):
        """Convert messages to Base64!"""
        response = requests.get('https://some-random-api.ml/base64?encode=' + message)
        data = response.json()
        # noinspection PyBroadException
        try:
            text = data.get('base64')
            baseEmbed = nextcord.Embed(title="Ay!? (Encoded!)", color=Colors.dark_grey, description=f"Ay \n```\n(\"{text}\")\n```", timestamp=ctx.message.created_at)
            return await ctx.send(embed=baseEmbed)
        except:
            return await ctx.send("Ay.. (An error has occurred.. maybe try again later..")

    @commands.command(usage='binary <message>')
    async def binary(self, ctx, *, message: str):
        """Convert images to Binary!"""
        response = requests.get('https://some-random-api.ml/binary?encode=' + message)
        data = response.json()
        # noinspection PyBroadException
        try:
            text = data.get('binary')
            binaryEmbed = nextcord.Embed(title="Ay!? (Encoded!)", color=Colors.dark_grey, description=f"Ay \n```\n(\"{text}\")\n```", timestamp=ctx.message.created_at)
            return await ctx.send(embed=binaryEmbed)
        except:
            return await ctx.send("Ay.. (An error has occurred.. maybe try again later..")

    async def cog_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'Ay!? (This command is missing arguments!? Use `manta cmd` to get arguments on commands!)')

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f'Ay!? (This command needs to cooldown!? Try in {round(error.retry_after, 2)} seconds)')

        await ctx.send(f"Ay.. (An error has occurred in my Entertainment Code.. I have sent the error out for assistance.)")

        occurredEmbed = nextcord.Embed(color=Colors.dark_grey,
                                       title="Ay.. (An error has occurred in my Entertainment Code..)", timestamp=ctx.message.created_at)
        occurredEmbed.add_field(name="Ay..! (Error Message!)",
                                value=f"*Ay..!?* ```py\n({error})\n```\n*Ay! (Error was in `{ctx.invoked_with}` command!)*", inline=False)
        occurredEmbed.add_field(name="Ay..! (Occurred Where!)",
                                value=f"*Ay! (**{ctx.guild.name}**)*", inline=False)

        await self.client.get_channel(1024070867057123399).send(embed=occurredEmbed)


def setup(client):
    client.add_cog(Entertainment(client))
