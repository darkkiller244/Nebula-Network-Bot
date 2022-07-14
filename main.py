from distutils import extension
import discord
import json
import os

from discord import Guild, app_commands
from discord.ext import commands


class Main(commands.Bot):
    
    def __init__(self):
        super().__init__(
            command_prefix = ".",
            intents = discord.Intents.all(),
            application_id=996142024430452826) # Client ID

    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="The Nebula Network"))

        print(f'{self.user} has initialized.')


    async def setup_hook(self):

        self.initial_extensions = [
            'cogs.core',

            'cogs.suggestion',
            'cogs.invite',
            'cogs.group',
            'cogs.ping',]

        for ext in self.initial_extensions:
            await self.load_extension(ext)

        # Guild ID
        await bot.tree.sync(guild=discord.Object(id=848367847670284298))


bot = Main()
bot.run(os.environ["DISCORD_TOKEN"])
#bot.run(os.environ['DISCORD_TOKEN'])
