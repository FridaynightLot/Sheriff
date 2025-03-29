import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from utils.db import Database
from config.config import ROLES, COLORS

db = Database()


class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="buy_role", description="Купить премиум роль")
    @app_commands.choices(
        role=[
            app_commands.Choice(name="VIP", value="VIP"),
            app_commands.Choice(name="PREMIUM", value="PREMIUM"),
            app_commands.Choice(name="ADMIN", value="ADMIN"),
        ]
    )
    async def buy_role(self, interaction: discord.Interaction, role: str):
        user_data = await db.get_or_create_user(interaction.user.id)
        role_data = ROLES[role]

        if user_data["balance"] < role_data["price"]:
            await interaction.response.send_message(
                f"❌ Недостаточно средств! Необходимо: {role_data['price']} монет",
                ephemeral=True,
            )
            return

        # Создаем роль на сервере, если её нет
        guild_role = discord.utils.get(interaction.guild.roles, name=role)
        if not guild_role:
            guild_role = await interaction.guild.create_role(
                name=role,
                color=discord.Color(role_data["color"]),
                permissions=discord.Permissions(
                    **{perm: True for perm in role_data["permissions"]}
                ),
            )

        # Добавляем роль пользователю
        await interaction.user.add_roles(guild_role)

        # Обновляем баланс и добавляем премиум статус
        await db.update_balance(interaction.user.id, -role_data["price"])
        expires_at = datetime.utcnow() + timedelta(days=30)
        await db.add_premium_role(interaction.user.id, role, expires_at)

        embed = discord.Embed(
            title="🎉 Поздравляем с покупкой!",
            description=f"Вы успешно приобрели роль {role}",
            color=discord.Color(COLORS["SUCCESS"]),
        )
        embed.add_field(name="Срок действия", value="30 дней")
        embed.add_field(name="Стоимость", value=f"{role_data['price']} монет")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="premium_status", description="Проверить статус премиум подписки"
    )
    async def premium_status(self, interaction: discord.Interaction):
        status = await db.get_premium_status(interaction.user.id)

        if not status:
            embed = discord.Embed(
                title="❌ Премиум статус отсутствует",
                description="У вас нет активной премиум подписки",
                color=discord.Color(COLORS["ERROR"]),
            )
        else:
            expires_at = status["expires_at"]
            days_left = (expires_at - datetime.utcnow()).days

            embed = discord.Embed(
                title="✨ Премиум статус",
                description=f"Роль: {status['role']}",
                color=discord.Color(ROLES[status["role"]]["color"]),
            )
            embed.add_field(name="Осталось дней", value=str(days_left))

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Premium(bot))
