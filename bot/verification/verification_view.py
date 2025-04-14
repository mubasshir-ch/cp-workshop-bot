import discord
from discord import Embed
from discord.ui import Modal
from typing import cast
from datetime import datetime, timezone

import bot.utils as utils
from bot.verification.verification_service import VerificationService
from .models import Verification


class VerificationView:
    def __init__(self, verification_service: VerificationService):
        self.verification_service = verification_service

    def get_verification_embed(self):
        embed = Embed(
            title="Verification",
            description="Click the button below to verify yourself.\nUse the email you used while registration.",
            color=discord.Color.blue(),
        )
        return embed

    def get_verification_view(self):
        view = discord.ui.View(timeout=None)

        button = discord.ui.Button(
            label="Verify", style=discord.ButtonStyle.green, custom_id="verify_button"
        )

        async def button_callback(interaction: discord.Interaction):
            guild = cast(discord.Member, interaction.user)
            verified_role = guild.get_role(
                self.verification_service.bot.VERIFIED_ROLE_ID
            )

            if verified_role in guild.roles:
                await interaction.respond(
                    content="You are already verified.",
                    ephemeral=True,
                )
                return

            modal = self.get_verification_modal()
            await interaction.response.send_modal(modal)

        button.callback = button_callback

        view.add_item(button)

        return view

    def get_verification_modal(self):
        modal = Modal(title="Verification", timeout=None)
        modal.add_item(discord.ui.InputText(label="Enter your email."))

        async def modal_callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)

            email = cast(str, modal.children[0].value)

            if not utils.is_valid_email(email):
                await interaction.respond(
                    content="Please enter a valid email address.",
                    ephemeral=True,
                )
                return

            try:
                verification = await self.verification_service.verify_email(
                    email, cast(discord.Member, interaction.user)
                )
                if verification.status == "CodeSent":
                    embed = Embed(
                        title="Verification Code Sent",
                        description=f"A verification code has been sent to `{verification.email}`.\nPlease check your inbox or spam folder.\nThe code will expire in 5 minutes.",
                        color=discord.Color.green(),
                    )

                    embed.set_footer(
                        text="If you don't receive the email, please click on the 'verify' button again."
                    )

                    await interaction.respond(
                        embed=embed,
                        view=self.get_code_verification_view(verification),
                        ephemeral=True,
                        delete_after=5 * 60,
                    )
                    return

                message_content = ""
                if verification.status == "EmailNotFound":
                    message_content = "Email not found. Make sure you use the email you registered with."
                elif verification.status == "AlreadyVerified":
                    message_content = "You are already verified."
                elif verification.status == "EmailAlreadyAssigned":
                    message_content = f"This email is already assigned to another user: `{verification.username}`. Please contact the admin if you think this is a mistake."

                assert message_content != ""

                await interaction.respond(
                    content=message_content,
                    ephemeral=True,
                )

                # await interaction.respond(content=resp, ephemeral=True)
            except Exception as e:
                await interaction.respond(
                    content=f"An error occurred: {str(e)}",
                    ephemeral=True,
                )

        modal.callback = modal_callback
        return modal

    def get_code_verification_view(self, verification: Verification):
        view = discord.ui.View(timeout=5 * 60)

        button = discord.ui.Button(
            label="Enter Code",
            style=discord.ButtonStyle.green,
        )

        async def button_callback(interaction: discord.Interaction):

            if self.verification_service.has_verification_code_expired(verification):
                await interaction.edit(
                    content="Verification code has expired. Please click the 'verify' button again.",
                    embed=None,
                    view=None,
                )
                return

            modal = self.get_code_verification_modal(verification)
            await interaction.response.send_modal(modal)

        button.callback = button_callback
        view.add_item(button)

        return view

    def get_code_verification_modal(self, verification):
        modal = Modal(title="Verification Code", timeout=None)

        modal.add_item(discord.ui.InputText(label="Enter the verification code."))

        async def modal_callback(interaction: discord.Interaction):

            await interaction.response.defer(ephemeral=True)

            if self.verification_service.has_verification_code_expired(verification):
                await interaction.edit(
                    content="Verification code has expired. Please click the 'verify' button again.",
                    embed=None,
                    view=None,
                )
                return

            code = cast(str, modal.children[0].value)

            if not code.isdigit():
                await interaction.respond(
                    content="Please enter a valid verification code.",
                    ephemeral=True,
                )
                return

            if int(code) != verification.code:
                await interaction.respond(
                    content="Invalid verification code. Please try again.",
                    ephemeral=True,
                )
                return

            try:
                await self.verification_service.complete_verification(
                    verification.email, cast(discord.Member, interaction.user)
                )
                verification.expires_at = datetime.now(timezone.utc)

                await interaction.edit(
                    content="You have been successfully verified!",
                    embed=None,
                    view=None,
                )

            except Exception as e:
                await interaction.respond(
                    content=f"An error occurred: {str(e)}",
                    ephemeral=True,
                )

        modal.callback = modal_callback
        return modal
