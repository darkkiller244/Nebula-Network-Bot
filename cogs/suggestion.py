from ast import alias
from cProfile import label
from logging import PlaceHolder
import discord

from discord import ActionRow, ButtonStyle, app_commands, ui
from discord.ui import Button
from discord.ext import commands
from datetime import datetime

class suggestion(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        bot.tree.on_error = self.on_command_error
        self.bot = bot
    
    @app_commands.command(name='suggestion',description='Submit a suggestion')
    @app_commands.checks.has_role('Verified')
    async def suggestion(self, interaction: discord.Interaction):
        await interaction.response.send_modal(suggestion_modal())


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


class suggestion_modal(ui.Modal, title="New Suggestion"):
    answer_one = ui.TextInput(
        label = "Suggestion Type",
        style = discord.InputTextStyle.short,
        placeholder='Game or Discord | If it\'s for a game please state which one',
        required=True,
        max_length=20
    )
    
    answer_two = ui.TextInput(
        label="Suggestion", 
        style = discord.TextStyle.long, 
        placeholder='Input the suggestion here', 
        required=True,
        max_length=500
    )

    async def on_submit(self, suggester_interaction: discord.Interaction):
        suggestion_embed = discord.Embed(
            title=self.title,
            description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}',
            timestamp=datetime.now(),
            color=0x3f6782 # Default
        )

        suggestion_embed.set_footer(text='Status: Pending\n')
        suggestion_embed.set_author(name=suggester_interaction.user, icon_url=suggester_interaction.user.avatar)

        review_channel = suggester_interaction.guild.get_channel(996956901722050571) or await suggester_interaction.guild.fetch_channel(996956901722050571)


        # Interaction response embed
        suggestion_response = discord.Embed(
            title='Suggestion Submitted!',
            description='Your suggestion has been sent for approval!\nOnce approved it will be posted in <#995767191267966977>',
            timestamp=datetime.now(),
            color=0x49ba8b) # Green                    


        class ConfirmationButtons(discord.ui.View):
            
            def __init__(self, answer_one, answer_two, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.answer_one = answer_one
                self.answer_two = answer_two


            @discord.ui.button(label="Accept", style=ButtonStyle.green)
            async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
                for item in self.children:
                    item.disabled = True
                await interaction.response.edit_message(view=self)
                self.stop()

                # Getting user that interacted with prompt
                user_name = str(interaction.user.name)

                # Embed for staff channel
                suggestion_embed = discord.Embed(
                    title='Suggestion Accepted',
                    description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}',
                    timestamp=datetime.now(),
                    color=0x49ba8b  # Green
                )

                suggestion_embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                suggestion_embed.set_footer(text=f'Accepted by {user_name}')

                # Updating suggestion in staff channel
                await interaction.message.edit(embed=suggestion_embed)

                # Embed for suggestion channel
                public_suggestion_embed = discord.Embed(
                    title="New Suggestion",
                    description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}',
                    timestamp=datetime.now(),
                    color=0x3f6782  # Default
                )

                public_suggestion_embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
                public_suggestion_embed.set_footer(text=f'Accepted by {user_name}')

                # Getting suggestion channel
                suggestion_channel = interaction.guild.get_channel(995767191267966977) or await interaction.guild.fetch_channel(995767191267966977)
                suggestion_message = await suggestion_channel.send(embed=public_suggestion_embed)

                # Adding UpVote/DownVote reactions
                await suggestion_message.add_reaction('<:UpVote:996957606822285343>')
                await suggestion_message.add_reaction('<:DownVote:996957630494937118>')

                # Create thread here
                await suggestion_message.create_thread(name="Suggestion Discussion", auto_archive_duration=10080)

            @discord.ui.button(label="Reject", style=ButtonStyle.red)
            async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
                for item in self.children:
                    item.disabled = True
                await interaction.response.edit_message(view=self)
                self.stop()
                
                # Getting user that interacted with prompt
                user_name = str(interaction.user.name)

                reason_embed = discord.Embed(
                    title="Reason for Rejection",
                    description=f"**Please provide the reason for rejecting:**\n{self.answer_two}",
                    color=0xef484a
                )
                
                reason_embed.remove_author()
                reason_embed.set_footer(text="❗ Choose carefully | This action cannot be reverted.")

                class ReasonButtons(discord.ui.View):
                    
                    def __init__(self, answer_one, answer_two, *args, **kwargs):
                        super().__init__(*args, **kwargs)
                        self.answer_one = answer_one
                        self.answer_two = answer_two

                    @discord.ui.button(label="Duplicate", style=ButtonStyle.primary)
                    async def reason_one(self, reason_one_interaction: discord.Interaction, button: discord.ui.Button):
                        for item in self.children:
                            item.disabled = True
                        await reason_one_interaction.response.edit_message(view=self)
                        self.stop()

                        reason = "Your suggestion has been rejected because\nit is too similar to a suggestion already made."
                        rejection_embed = discord.Embed(
                            title="Suggestion Rejected",
                            description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}\n\n**Reason**\n{reason}',
                            timestamp=datetime.now(),
                            color=0xef484a  # Red
                        )

                        staff_rejection_embed = discord.Embed(
                            title="Suggestion Rejected",
                            description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}\n\n**Reason:** Duplicate',
                            timestamp=datetime.now(),
                            color=0xef484a  # Red
                        )

                        # Updating footer of embed with user & timestamp
                        rejection_embed.remove_author()
                        rejection_embed.set_footer(text=f"Rejected by {user_name}")
                        staff_rejection_embed.set_author(name=suggester_interaction.user, icon_url=suggester_interaction.user.avatar)
                        staff_rejection_embed.set_footer(text=f"Rejected by {user_name}")

                        # Updating suggestion in staff channel
                        await interaction.message.edit(embed=staff_rejection_embed)

                        # Alerting user of rejected suggestion
                        await suggester_interaction.user.send(embed=rejection_embed)
                    
                    @discord.ui.button(label="Unrealistic", style=ButtonStyle.primary)
                    async def reason_two(self, reason_two_interaction: discord.Interaction, button: discord.ui.Button):
                        for item in self.children:
                            item.disabled = True
                        await reason_two_interaction.response.edit_message(view=self)
                        self.stop()

                        reason = "Your suggestion has been rejected because\nit will not be feasible due to either roblox limitations, development limitations, or not intune with the game idea."
                        rejection_embed = discord.Embed(
                            title='Suggestion Rejected',
                            description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}\n\n**Reason**\n{reason}',
                            timestamp=datetime.now(),
                            color=0xef484a  # Red
                        )

                        staff_rejection_embed = discord.Embed(
                            title="Suggestion Rejected",
                            description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}\n\n**Reason:** {button.label}',
                            timestamp=datetime.now(),
                            color=0xef484a  # Red
                        )

                        # Updating footer of embed with user & timestamp
                        rejection_embed.remove_author()
                        rejection_embed.set_footer(text=f"Rejected by {user_name}")
                        staff_rejection_embed.set_footer(text=f"Rejected by {user_name}")

                        # Updating suggestion in staff channel
                        staff_rejection_embed.set_author(name=suggester_interaction.user, icon_url=suggester_interaction.user.avatar)
                        await interaction.message.edit(embed=staff_rejection_embed)

                        # Alerting user of rejected suggestion
                        await suggester_interaction.user.send(embed=rejection_embed)

                    @discord.ui.button(label="Inappropriate", style=ButtonStyle.danger)
                    async def reason_three(self, reason_three_interaction: discord.Interaction, button: discord.ui.Button):
                        for item in self.children:
                            item.disabled = True
                        await reason_three_interaction.response.edit_message(view=self)
                        self.stop()

                        reason = "Your suggestion has been rejected because\nof inappropriate content."
                        rejection_embed = discord.Embed(
                            title='Suggestion Rejected',
                            description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}\n\n**Reason**\n{reason}',
                            timestamp=datetime.now(),
                            color=0xef484a  # Red
                        )

                        staff_rejection_embed = discord.Embed(
                            title="Suggestion Rejected",
                            description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}\n\n**Reason:** {button.label}',
                            timestamp=datetime.now(),
                            color=0xef484a  # Red
                        )

                        # Updating footer of embed with user & timestamp
                        rejection_embed.remove_author()
                        rejection_embed.set_footer(text=f"Rejected by {user_name}")

                        staff_rejection_embed.set_author(name=suggester_interaction.user, icon_url=suggester_interaction.user.avatar)
                        staff_rejection_embed.set_footer(text=f"Rejected by {user_name}")

                        # Updating suggestion in staff channel
                        await interaction.message.edit(embed=staff_rejection_embed)

                        # Alerting user of rejected suggestion
                        await suggester_interaction.user.send(embed=rejection_embed)

                    @discord.ui.button(label="Troll Request", style=ButtonStyle.danger)
                    async def reason_four(self, reason_four_interaction: discord.Interaction, button: discord.ui.Button):
                        for item in self.children:
                            item.disabled = True
                        await reason_four_interaction.response.edit_message(view=self)
                        self.stop()

                        reason = "Your suggestion has been rejected and\ndeemed a troll request, further suggestions of\nthis type may lead to punishment."
                        rejection_embed = discord.Embed(
                            title='Suggestion Rejected',
                            description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}\n\n**Reason**\n{reason}',
                            timestamp=datetime.now(),
                            color=0xef484a  # Red
                        )

                        staff_rejection_embed = discord.Embed(
                            title="Suggestion Rejected",
                            description=f'**{self.answer_one.label}**\n{self.answer_one}\n\n**{self.answer_two.label}**\n{self.answer_two}\n\n**Reason:** {button.label}',
                            timestamp=datetime.now(),
                            color=0xef484a  # Red
                        )

                        # Updating footer of embed with user & timestamp
                        rejection_embed.remove_author()
                        rejection_embed.set_footer(text=f"Rejected by {user_name}")

                        staff_rejection_embed.set_author(name=suggester_interaction.user, icon_url=suggester_interaction.user.avatar)
                        staff_rejection_embed.set_footer(text=f"Rejected by {user_name}")

                        # Updating suggestion in staff channel
                        await interaction.message.edit(embed=staff_rejection_embed)

                        # Alerting user of rejected suggestion
                        await suggester_interaction.user.send(embed=rejection_embed)

                    @discord.ui.button(label="Other", style=ButtonStyle.grey)
                    async def other(self, other_interaction: discord.Interaction, button: discord.ui.Button):
                        for item in self.children:
                            item.disabled = True
                        await other_interaction.response.edit_message(view=self)
                        self.stop()
                    
                # Prompting reason for rejection
                await interaction.followup.send(embed=reason_embed, ephemeral=True, view=ReasonButtons(answer_one=self.answer_one, answer_two=self.answer_two))

        suggestion_response.set_author(name=suggester_interaction.user, icon_url=suggester_interaction.user.avatar)
        await suggester_interaction.response.send_message(embed=suggestion_response, ephemeral=True)

        await review_channel.send(embed=suggestion_embed, view=ConfirmationButtons(answer_one=self.answer_one, answer_two=self.answer_two))

            



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        suggestion(bot),
        guilds=[discord.Object(id=848367847670284298)]
    )
    