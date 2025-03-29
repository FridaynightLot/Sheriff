import discord
from discord.ext import commands, tasks
from datetime import datetime
from utils.db import Database

db = Database()


class PremiumCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_premium_roles.start()

    def cog_unload(self):
        self.check_premium_roles.cancel()

    @tasks.loop(hours=1)
    async def check_premium_roles(self):
        now = datetime.utcnow()
        async for premium_user in db.premium_users.find():
            if premium_user["expires_at"] <= now:
                user_id = premium_user["_id"]
                role_name = premium_user["role"]

                # Получаем пользователя и удаляем роль
                for guild in self.bot.guilds:
                    member = guild.get_member(user_id)
                    if member:
                        role = discord.utils.get(guild.roles, name=role_name)
                        if role:
                            try:
                                await member.remove_roles(role)
                                # Отправляем уведомление пользователю
                                try:
                                    await member.send(
                                        f"❌ Ваша роль {role_name} истекла! "
                                        "Вы можете продлить её, купив снова."
                                    )
                                except:
                                    pass  # Не можем отправить DM
                            except:
                                continue

                # Удаляем запись из базы данных
                await db.remove_premium_role(user_id)

    @check_premium_roles.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(PremiumCheck(bot))
