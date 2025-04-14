import discord
from discord.ext import commands
from typing import cast

from bot import BotSubclass
from bot.verification import verification_view
from bot.verification.verification_service import VerificationService
from bot.verification.verification_view import VerificationView

class Verification(commands.Cog):
    def __init__(self, bot:BotSubclass, verification_service:VerificationService, verification_view: VerificationView):
        self.bot = bot
        self.bot.loop.create_task(self.setup_message())
        self.verification_service = verification_service
        self.verification_view = verification_view
    
    async def setup_message(self):
        await self.bot.wait_until_ready()
        verification_channel = cast(discord.TextChannel, self.bot.get_channel(self.bot.VERIFICATION_CHANNEL_ID))
        message = await verification_channel.fetch_message(self.bot.VERIFICATION_MESSAGE_ID)

        embed = self.verification_view.get_verification_embed()
        view = self.verification_view.get_verification_view()

        await message.edit(content="", embed = embed, view = view)

    


def setup(bot:BotSubclass):
    verification_service = VerificationService(bot)
    verification_view = VerificationView(verification_service)
    bot.add_cog(Verification(bot, verification_service, verification_view))
