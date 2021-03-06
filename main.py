
import discord, os

from discord.ext import commands

class aclient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', 
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="the Nebula Network"))
        
    async def setup_hook(self):

        self.initial_extensions = [
            'cogs.core',

            'cogs.suggestion',
            'cogs.invite',
            'cogs.group',
            'cogs.ping']

        for ext in self.initial_extensions:
            await self.load_extension(ext)
            print(f'{ext} loaded')

        await client.tree.sync()
        print(f'\n{self.user} has initialized.')


client = aclient()
client.run(os.environ["DISCORD_TOKEN"])