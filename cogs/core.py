from datetime import datetime
import discord

from discord import app_commands
from discord.ext import commands


class critical(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        bot.tree.on_error = self.on_command_error
        self.bot = bot

    initial_extensions = [
        'cogs.suggestion',
        'cogs.invite',
        'cogs.group',
        'cogs.ping', ]

    # Auto complete testing function.
    #def autocompletion(interaction: discord.AutocompleteInterarction):
    #    return [(x, x) for x in initial_extensions]


    @app_commands.command(name='load', description='Enable a command')
    @app_commands.describe(command_name="Command name")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.has_role('Verified')
    async def load(self, interaction: discord.Interaction, command_name: str):
        if command_name in ['all', '*']:

            for ext in self.initial_extensions:
                # If cog not loaded
                print(ext[5:])
                if ext[5:] not in self.bot.cogs.keys():
                    print(ext)
                    await self.bot.load_extension(ext)

            load_embed = discord.Embed(
                title='All Commands Loaded',
                description=f'All available commands have been successfully **loaded.**',
                timestamp=datetime.now(),
                color=0x49ba8b)  # Green

            load_log_embed = discord.Embed(
                title='All Commands Loaded',
                description=f'{interaction.user} loaded all available extensions.',
                timestamp=datetime.now(),
                color=0x3f6782)  # Default

            load_embed.set_footer(text='All Commands Enabled')
            load_log_embed.set_footer(text='All Commands Enabled')
            await interaction.response.send_message(embed=load_embed, ephemeral=True)

            log_channel = interaction.guild.get_channel(996958366343647272) or await interaction.guild.fetch_channel(996958366343647272)
            await log_channel.send(embed=load_log_embed)

        elif command_name not in ['main', 'core']:
            await self.bot.load_extension(f'cogs.{command_name}')

            load_embed = discord.Embed(
                title='Command Loaded',
                description=f'The requested command has been successfully **loaded**.',
                timestamp=datetime.now(),
                color=0x49ba8b)  # Green

            load_log_embed = discord.Embed(
                title='Command Loaded',
                description=f'{interaction.user} loaded the **{command_name}** extension.',
                timestamp=datetime.now(),
                color=0x3f6782)  # Default

            load_embed.set_footer(text='Command Enabled')
            load_log_embed.set_footer(text='Command Enabled')
            await interaction.response.send_message(embed=load_embed, ephemeral=True)

            log_channel = interaction.guild.get_channel(996958366343647272) or await interaction.guild.fetch_channel(996958366343647272)
            await log_channel.send(embed=load_log_embed)

        elif command_name in ['main', 'core']:
            core_embed = discord.Embed(
                    title='Access Denied',
                    description=f'You are not authorized to enable core extensions.\nIf you believe this is a mistake, it\'s not.',
                    timestamp=datetime.now(),
                    color=0xef484a)  # Red

            core_embed.set_footer(text='Invalid Permission')
            await interaction.response.send_message(embed=core_embed, ephemeral=True)

    # Disables a command
    @app_commands.command(name='unload', description='Disable a command')
    @app_commands.describe(command_name="Command name")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.has_role('Verified')
    async def unload(self, interaction: discord.Interaction, command_name: str):
        if command_name in ['all', '*']:

            for ext in self.initial_extensions:
                # If cog loaded
                print(ext[5:])
                if ext[5:] in self.bot.cogs.keys():
                    print(ext)
                    await self.bot.unload_extension(ext)

            unload_embed = discord.Embed(
                title='All Commands Unloaded',
                description=f'All available commands have been successfully **unloaded**.',
                timestamp=datetime.now(),
                color=0x49ba8b)  # Green

            unload_log_embed = discord.Embed(
                title='All Commands Unloaded',
                description=f'{interaction.user} unloaded all available extensions.',
                timestamp=datetime.now(),
                color=0x3f6782)  # Default

            unload_embed.set_footer(text='All Commands Disabled')
            unload_log_embed.set_footer(text='All Commands Disabled')
            await interaction.response.send_message(embed=unload_embed, ephemeral=True)

            log_channel = interaction.guild.get_channel(996958366343647272) or await interaction.guild.fetch_channel(996958366343647272)
            await log_channel.send(embed=unload_log_embed)

        elif command_name not in ['main', 'core']:
            await self.bot.unload_extension(f'cogs.{command_name}')

            unload_embed = discord.Embed(
                title='Command Unloaded',
                description=f'The requested command has been successfully **unloaded**.',
                timestamp=datetime.now(),
                color=0x49ba8b)  # Green

            unload_log_embed = discord.Embed(
                title='Command Unloaded',
                description=f'{interaction.user} unloaded the **{command_name}** extension.',
                timestamp=datetime.now(),
                color=0x3f6782)  # Default

            unload_embed.set_footer(text='Command Disabled')
            unload_log_embed.set_footer(text='Command Disabled')
            await interaction.response.send_message(embed=unload_embed, ephemeral=True)

            log_channel = interaction.guild.get_channel(996958366343647272) or await interaction.guild.fetch_channel(996958366343647272)
            await log_channel.send(embed=unload_log_embed)

        elif command_name in ['main', 'core']:
            core_embed = discord.Embed(
                title='Access Denied',
                description=f'You are not authorized to disable core extensions.\nIf you believe this is a mistake, it\'s not.',
                timestamp=datetime.now(),
                color=0xef484a)  # Red

            core_embed.set_footer(text='Invalid Permission')
            await interaction.response.send_message(embed=core_embed, ephemeral=True)

    # Reloads a command
    @app_commands.command(name='reload', description='Reload a command')
    @app_commands.describe(command_name="Command name")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.has_role('Verified')
    async def reload(self, interaction: discord.Interaction, command_name: str):
        if command_name in ['all', '*']:

            for ext in self.initial_extensions:
                await self.bot.reload_extension(ext)

            reload_embed = discord.Embed(
                title='All Commands Reloaded',
                description=f'All available commands have been successfully **reloaded**.',
                timestamp=datetime.now(),
                color=0x49ba8b)  # Green

            reload_log_embed = discord.Embed(
                title='All Commands Reloaded',
                description=f'{interaction.user} reloaded all available extensions.',
                timestamp=datetime.now(),
                color=0x3f6782)  # Default

            reload_embed.set_footer(text='All Commands Enabled')
            reload_log_embed.set_footer(text='All Commands Enabled')
            await interaction.response.send_message(embed=reload_embed, ephemeral=True)

            log_channel = interaction.guild.get_channel(996958366343647272) or await interaction.guild.fetch_channel(996958366343647272)
            await log_channel.send(embed=reload_log_embed)

        elif command_name not in ['main', 'core']:
            await self.bot.unload_extension(f'cogs.{command_name}')
            await self.bot.load_extension(f'cogs.{command_name}')

            reload_embed = discord.Embed(
                title='Command reloaded',
                description=f'The requested command has been successfully **reloaded**.',
                timestamp=datetime.now(),
                color=0x49ba8b)  # Green

            reload_log_embed = discord.Embed(
                title='Command Reloaded',
                description=f'{interaction.user} reloaded the **{command_name}** extension.',
                timestamp=datetime.now(),
                color=0x3f6782)  # Default

            reload_embed.set_footer(text='Command Enabled')
            reload_log_embed.set_footer(text='Command Enabled')
            await interaction.response.send_message(embed=reload_embed, ephemeral=True)

            log_channel = interaction.guild.get_channel(996958366343647272) or await interaction.guild.fetch_channel(996958366343647272)
            await log_channel.send(embed=reload_log_embed)

        elif command_name in ['main', 'core']:
            core_embed = discord.Embed(
                title='Access Denied',
                description=f'You are not authorized to disable core extensions.\nIf you believe this is a mistake, it\'s not.',
                timestamp=datetime.now(),
                color=0xef484a)  # Red

            core_embed.set_footer(text='Invalid Permission')
            await interaction.response.send_message(embed=core_embed, ephemeral=True)


    error_nosetup_embed = discord.Embed(
        title='Command Failed',
        description=f'The requested extension you tried to **load** does not exist.\nIf you believe this is a mistake please contact <@232236405466595328>',
        timestamp=datetime.now(),
        color=0xef484a  # Red
    )

    error_notloaded_embed = discord.Embed(
        title='Command Failed',
        description=f'The requested extension you tried to unload is already unloaded.\nIf you believe this is a mistake please contact <@232236405466595328>',
        timestamp=datetime.now(),
        color=0xef484a  # Red
    )

    error_loaded_embed = discord.Embed(
        title='Command Failed',
        description=f'The requested extension you tried to load is already loaded.\nIf you believe this is a mistake please contact <@232236405466595328>',
        timestamp=datetime.now(),
        color=0xef484a  # Red
    )

    error_nopermission_embed = discord.Embed(
        title='Command Failed',
        description=f'You do not have the proper permissions to run this command.\nIf you believe this is a mistake please contact <@232236405466595328>',
        timestamp=datetime.now(),
        color=0xef484a  # Red
    )

    error_failed_embed = discord.Embed(
        title='Command Failed',
        description=f'Failed to get the requested extension.\nPlease contact <@232236405466595328>',
        timestamp=datetime.now(),
        color=0xef484a  # Red
    )


    async def on_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error.original, commands.errors.ExtensionNotLoaded):
            await interaction.response.send_message(embed=self.error_notloaded_embed, ephemeral=True)

        elif isinstance(error.original, commands.errors.ExtensionAlreadyLoaded):
            await interaction.response.send_message(embed=self.error_loaded_embed, ephemeral=True)
        
        elif isinstance(error.original, commands.errors.ExtensionNotFound):
            await interaction.response.send_message(embed=self.error_nosetup_embed, ephemeral=True)

        elif isinstance(error.original, commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=self.error_nopermission_embed, ephemeral=True)

        elif isinstance(error.original, commands.errors.MissingRole):
            await interaction.response.send_message(embed=self.error_nopermission_embed, ephemeral=True)

        else:
            await interaction.response.send_message(embed=self.error_failed_embed, ephemeral=True)
            raise error.original


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        critical(bot),
        guilds=[discord.Object(id=848367847670284298)],
    )
