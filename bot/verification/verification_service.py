import discord
from typing import cast
import smtplib
from email.message import EmailMessage
import random
from datetime import datetime, timezone, timedelta

from bot import BotSubclass
from .models import User, Verification


class VerificationService:

    def __init__(self, bot: BotSubclass):
        self.bot = bot
        self.db = bot.db_service.db

    async def verify_email(self, email: str, member: discord.Member) -> Verification:

        existing_user = await self.get_assigned_user(email)

        if not existing_user:
            return Verification("EmailNotFound", email)

        if existing_user.username != "":
            if existing_user.username == member.name:
                return Verification("AlreadyVerified", email, member.name)

            return Verification("EmailAlreadyAssigned", email, existing_user.username)

        code, expires_at = self.generate_verification_code()
        await self.send_verification_email(email, code)

        return Verification("CodeSent", email, existing_user.username, code, expires_at)

    async def get_assigned_user(self, email: str) -> User | None:

        users_collection = self.db["users"]
        user = await users_collection.find_one({"email": email})

        if not user:
            return None
        return User.from_dict(user)

    def generate_verification_code(self):
        code = random.randint(100000, 999999)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
        return code, expires_at

    async def send_verification_email(self, recipient_email: str, code: int):
        from_email = self.bot.VERIFICATION_SENDER_EMAIL
        apppassword = self.bot.VERIFICATION_SENDER_PASSWORD

        msg = EmailMessage()
        msg["Subject"] = (
            "Brac University Competitive Programming Workshop 2025 discord server verification code"
        )
        msg["From"] = from_email

        msg["To"] = recipient_email

        msg.set_content(
            f"Your verification code is {code}. It will expire in 5 minutes.\n\n"
            "If you did not request this email, please ignore it."
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, apppassword)
            smtp.send_message(msg)

    def has_verification_code_expired(self, verification: Verification) -> bool:
        if verification.expires_at is None:
            return True
        return datetime.now(timezone.utc) > verification.expires_at

    async def complete_verification(self, email: str, member: discord.Member):

        users_collection = self.db["users"]

        await users_collection.update_one(
            {"email": email},
            {
                "$set": {
                    "username": member.name,
                }
            },
        )
        guild = member.guild
        verified_role = guild.get_role(self.bot.VERIFIED_ROLE_ID)

        if not verified_role:
            raise ValueError("Verified role not found in the guild. Contact Admin")
        await member.add_roles(verified_role)
