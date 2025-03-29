import discord
from discord import app_commands
from discord.ext import commands
from utils.checks import premium_only, has_role
from utils.db import Database
from config.config import COLORS
import random

db = Database()

class PremiumFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="mass_dm", description="Отправить сообщение всем участникам (ADMIN)")
    @has_role("ADMIN")
    async def mass_dm(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)
        
        success = 0
        failed = 0
        
        for member in interaction.guild.members:
            try:
                await member.send(message)
                success += 1
            except:
                failed += 1
                
        embed = discord.Embed(
            title="📨 Массовая рассылка завершена",
            color=discord.Color(COLORS['SUCCESS'])
        )
        embed.add_field(name="✅ Успешно отправлено", value=str(success))
        embed.add_field(name="❌ Не удалось отправить", value=str(failed))
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    @app_commands.command(name="custom_role", description="Создать кастомную роль (PREMIUM)")
    @has_role("PREMIUM")
    async def custom_role(
        self,
        interaction: discord.Interaction,
        name: str,
        color: str
    ):
        try:
            # Конвертируем hex в int
            color_int = int(color.strip('#'), 16)
            
            # Создаем роль
            role = await interaction.guild.create_role(
                name=name,
                color=discord.Color(color_int),
                reason=f"Кастомная роль создана {interaction.user}"
            )
            
            # Добавляем роль пользователю
            await interaction.user.add_roles(role)
            
            embed = discord.Embed(
                title="✨ Роль создана",
                description=f"Роль {role.mention} успешно создана и добавлена",
                color=discord.Color(color_int)
            )
            await interaction.response.send_message(embed=embed)
            
        except ValueError:
            await interaction.response.send_message(
                "❌ Неверный формат цвета! Используйте HEX формат (#FFFFFF)",
                ephemeral=True
            )
            
    @app_commands.command(name="multiply_xp", description="Умножить опыт за сообщения (VIP)")
    @has_role("VIP")
    @app_commands.choices(multiplier=[
        app_commands.Choice(name="x2", value=2),
        app_commands.Choice(name="x3", value=3),
        app_commands.Choice(name="x4", value=4)
    ])
    async def multiply_xp(self, interaction: discord.Interaction, multiplier: int, duration: int):
        # Здесь будет логика умножения опыта
        embed = discord.Embed(
            title="🌟 Множитель опыта активирован",
            description=f"Множитель x{multiplier} на {duration} минут",
            color=discord.Color(COLORS['SUCCESS'])
        )
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="custom_embed", description="Создать красивое сообщение (PREMIUM)")
    @has_role("PREMIUM")
    async def custom_embed(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        color: str
    ):
        try:
            color_int = int(color.strip('#'), 16)
            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color(color_int)
            )
            embed.set_footer(text=f"Создано {interaction.user}")
            
            await interaction.response.send_message(embed=embed)
            
        except ValueError:
            await interaction.response.send_message(
                "❌ Неверный формат цвета! Используйте HEX формат (#FFFFFF)",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(PremiumFeatures(bot)) 