import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from utils.db import Database
from utils.checks import premium_only
from config.config import COLORS
import random

db = Database()


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Проверить баланс")
    async def balance(self, interaction: discord.Interaction):
        user_data = await db.get_or_create_user(interaction.user.id)

        embed = discord.Embed(
            title="💰 Баланс",
            description=f"У вас {user_data['balance']} монет",
            color=discord.Color(COLORS["INFO"]),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="Получить ежедневную награду")
    async def daily(self, interaction: discord.Interaction):
        user_data = await db.get_or_create_user(interaction.user.id)
        now = datetime.utcnow()

        if user_data.get("daily_last_claim"):
            last_claim = user_data["daily_last_claim"]
            if isinstance(last_claim, str):
                last_claim = datetime.fromisoformat(last_claim)

            if now - last_claim < timedelta(days=1):
                next_claim = last_claim + timedelta(days=1)
                time_left = next_claim - now
                hours = time_left.seconds // 3600
                minutes = (time_left.seconds % 3600) // 60

                embed = discord.Embed(
                    title="⏰ Награда еще не доступна",
                    description=f"Приходите через {hours} часов и {minutes} минут",
                    color=discord.Color(COLORS["WARNING"]),
                )
                await interaction.response.send_message(embed=embed)
                return

        # Базовая награда
        reward = 100

        # Проверяем премиум статус для бонуса
        premium_status = await db.get_premium_status(interaction.user.id)
        if premium_status:
            if premium_status["role"] == "VIP":
                reward *= 2
            elif premium_status["role"] == "PREMIUM":
                reward *= 3
            elif premium_status["role"] == "ADMIN":
                reward *= 4

        await db.update_balance(interaction.user.id, reward)
        await db.users.update_one(
            {"_id": interaction.user.id}, {"$set": {"daily_last_claim": now}}
        )

        embed = discord.Embed(
            title="🎁 Ежедневная награда получена!",
            description=f"Вы получили {reward} монет",
            color=discord.Color(COLORS["SUCCESS"]),
        )
        if premium_status:
            embed.add_field(
                name="✨ Премиум бонус", value=f"Бонус за роль {premium_status['role']}"
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="work", description="Заработать монеты")
    @app_commands.cooldown(1, 3600)  # Раз в час
    async def work(self, interaction: discord.Interaction):
        base_reward = random.randint(50, 150)

        # Проверяем премиум статус для бонуса
        premium_status = await db.get_premium_status(interaction.user.id)
        reward = base_reward

        if premium_status:
            if premium_status["role"] == "VIP":
                reward = int(base_reward * 1.5)
            elif premium_status["role"] == "PREMIUM":
                reward = int(base_reward * 2)
            elif premium_status["role"] == "ADMIN":
                reward = int(base_reward * 2.5)

        await db.update_balance(interaction.user.id, reward)

        embed = discord.Embed(
            title="💼 Работа выполнена!",
            description=f"Вы заработали {reward} монет",
            color=discord.Color(COLORS["SUCCESS"]),
        )
        if premium_status:
            embed.add_field(
                name="✨ Премиум бонус", value=f"Бонус за роль {premium_status['role']}"
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Economy(bot))
