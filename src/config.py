import os
from dotenv import load_dotenv

load_dotenv()

# Discord конфигурация
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")

# Цвета для эмбедов
COLORS = {"SUCCESS": 0x2ECC71, "ERROR": 0xE74C3C, "WARNING": 0xF1C40F, "INFO": 0x3498DB}

# Роли
ROLES = {
    "VIP": {
        "name": "VIP",
        "price": 100,
        "color": 0xF1C40F,
        "permissions": ["view_channel", "send_messages", "embed_links", "attach_files"],
    },
    "PREMIUM": {
        "name": "PREMIUM",
        "price": 300,
        "color": 0xE91E63,
        "permissions": [
            "view_channel",
            "send_messages",
            "embed_links",
            "attach_files",
            "manage_messages",
        ],
    },
    "ADMIN": {
        "name": "ADMIN",
        "price": 500,
        "color": 0x9B59B6,
        "permissions": ["administrator"],
    },
}

# MongoDB конфигурация
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "sheriffbot"
