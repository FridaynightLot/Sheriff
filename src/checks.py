import discord
from discord import app_commands
from discord.ext import commands
from .db import Database
from config.config import ROLES

db = Database()

def premium_only():
    async def predicate(interaction: discord.Interaction):
        is_premium = await db.is_premium(interaction.user.id)
        if not is_premium:
            await interaction.response.send_message(
                "❌ Эта команда доступна только для премиум пользователей!",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)

def has_role(role_name: str):
    async def predicate(interaction: discord.Interaction):
        if role_name not in ROLES:
            return False
            
        user_premium = await db.get_premium_status(interaction.user.id)
        if not user_premium or user_premium['role'] != role_name:
            await interaction.response.send_message(
                f"❌ Эта команда доступна только для пользователей с ролью {role_name}!",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate) 