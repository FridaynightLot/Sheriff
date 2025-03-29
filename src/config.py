import os
from dotenv import load_dotenv

load_dotenv()

# Discord конфигурация
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')

# Цвета для эмбедов
COLORS = {
    'SUCCESS': 0x2ecc71,
    'ERROR': 0xe74c3c,
    'WARNING': 0xf1c40f,
    'INFO': 0x3498db
}

# Роли
ROLES = {
    'VIP': {
        'name': 'VIP',
        'price': 100,
        'color': 0xf1c40f,
        'permissions': ['view_channel', 'send_messages', 'embed_links', 'attach_files']
    },
    'PREMIUM': {
        'name': 'PREMIUM',
        'price': 300,
        'color': 0xe91e63,
        'permissions': ['view_channel', 'send_messages', 'embed_links', 'attach_files', 'manage_messages']
    },
    'ADMIN': {
        'name': 'ADMIN',
        'price': 500,
        'color': 0x9b59b6,
        'permissions': ['administrator']
    }
}

# MongoDB конфигурация
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = 'sheriffbot' 