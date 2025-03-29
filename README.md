# Sheriff Discord Bot

Многофункциональный Discord бот с возможностями модерации, музыки и развлечений.

## Возможности

- 🛡️ **Модерация**: ban, kick, mute, clear
- 🎵 **Музыка**: play, skip, queue, stop
- 🎮 **Игры**: game, leaderboard, daily, inventory
- 💎 **Роли**: VIP, PREMIUM, ADMIN

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/DiscordSheriffBot.git
cd DiscordSheriffBot
```

2. run: 
``` bash 
docker compose up --build app
```

## Структура проекта

```
DiscordSheriffBot/
├── commands/        # Команды бота
├── config/         # Конфигурационные файлы
├── events/         # Обработчики событий
├── utils/          # Вспомогательные функции
├── main.py         # Основной файл бота
├── requirements.txt # Зависимости
└── .env           # Конфигурация окружения
```

## Лицензия

MIT License 