from xmlrpc.client import DateTime
import discord

from discord import app_commands
from discord.ext import commands
from datetime import datetime


class invite(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        bot.tree.on_error = self.on_command_error
        self.bot = bot

    @app_commands.command(name='invite',description='Sends the link to the Discord')
    @app_commands.checks.has_role('Verified')
    async def invite(self, interaction: discord.Interaction):

        invite_embed = discord.Embed(
            title="Invite your Friends!",
            description="Get your friends to join so you can both be apart of the community!\n\nhttps://discord.gg/tb5eU23vzC",
            timestamp=datetime.now(),
            color=0x3f6782)

        await interaction.response.send_message(embed=invite_embed)


    error_nopermission_embed = discord.Embed(
            title='Command Failed',
            description=f'You do not have the proper permissions to run this command.\nIf you believe this is a mistake please contact <@232236405466595328>',
            timestamp=datetime.now(),
            color=0xef484a  # Red
        )

    error_notenabled_embed = discord.Embed(
        title='Command Failed',
        description=f'The requested command is not loaded.\nPlease try again later or request for it to be enabled.',
        timestamp=datetime.now(),
        color=0xef484a  # Red
    )

    error_failed_embed = discord.Embed(
        title='Command Failed',
        description=f'Failed to update trade request.\nPlease contact <@232236405466595328>',
        timestamp=datetime.now(),
        color=0xef484a  # Red
    )

    async def on_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(embed=self.error_nopermission_embed, ephemeral=True)

        elif isinstance(error, app_commands.errors.MissingRole):
            await interaction.response.send_message(embed=self.error_nopermission_embed, ephemeral=True)

        elif isinstance(error, app_commands.errors.CommandNotFound):
            await interaction.response.send_message(embed=self.error_notenabled_embed, ephemeral=True)

        else:
            await interaction.response.send_message(embed=self.error_failed_embed, ephemeral=True)
            raise error


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(invite(bot))

        