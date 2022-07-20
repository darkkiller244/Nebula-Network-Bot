
import discord

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
client.run('OTk2MTQyMDI0NDMwNDUyODI2.GZL6Du.gadlRZDDnYQRbce7ywvNRsGrY77Ggd_Ju1pEl0')
#bot.run(os.environ["DISCORD_TOKEN"])