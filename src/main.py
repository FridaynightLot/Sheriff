import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
APP_ID = os.getenv('APPLICATION_ID')

try:
    APP_ID = int(APP_ID)
except ValueError:
    raise ValueError(f"APPLICATION_ID должен быть числом, получено: {APP_ID}")

# Настройка интентов
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

class SheriffBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='/',
            intents=intents,
            application_id=APP_ID
        )
        
    async def setup_hook(self):
        logger.info("Загрузка когов...")
        for folder in ['commands', 'events']:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    if filename.endswith('.py'):
                        try:
                            await self.load_extension(f'{folder}.{filename[:-3]}')
                            logger.info(f"Загружен ког {folder}.{filename[:-3]}")
                        except Exception as e:
                            logger.error(f"Ошибка при загрузке кога {folder}.{filename[:-3]}: {str(e)}")
        
        try:
            logger.info("Синхронизация команд...")
            await self.tree.sync()
            logger.info("Команды синхронизированы")
        except Exception as e:
            logger.error(f"Ошибка при синхронизации команд: {str(e)}")

    async def on_ready(self):
        logger.info(f'Бот {self.user} готов к работе!')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name='за порядком'
            )
        )

async def main():
    print("Iam alive!")
    try:
        async with SheriffBot() as bot:
            await bot.start(TOKEN)
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main()) 
