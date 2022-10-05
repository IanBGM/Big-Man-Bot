import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv, find_dotenv
from loggerpy import Logger

client = commands.Bot(command_prefix=commands.when_mentioned_or('manta '), intents=nextcord.Intents.all(), help_command=None)

logger = Logger()
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")


@client.command(usage="load <extension>")
@commands.is_owner()
async def load(ctx, extension, folder=None):
    """Loads extensions!"""
    if folder is not None:
        client.load_extension(f'cogs.{folder}.{extension}')
    else:
        client.load_extension(f'cogs.{extension}')
    ctx.send(f'Ay! ({extension} loaded!)')


@client.command(usage="unload <extension>")
@commands.is_owner()
async def unload(ctx, extension, folder=None):
    """Unloads extensions!"""
    if folder is not None:
        client.unload_extension(f'cogs.{folder}.{extension}')
    else:
        client.unload_extension(f'cogs.{extension}')
    ctx.send(f'Ay! ({extension} unloaded!)')


@client.command(usage="reload <extension>")
@commands.is_owner()
async def reload(ctx, extension, folder=None):
    """Reloads extensions!"""
    if folder is not None:
        client.unload_extension(f'cogs.{folder}.{extension}')
        client.load_extension(f'cogs.{folder}.{extension}')
    else:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Ay! ({extension} reloaded!)')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

for filename in os.listdir('cogs/Interaction'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.Interaction.{filename[:-3]}')

client.run(TOKEN)
