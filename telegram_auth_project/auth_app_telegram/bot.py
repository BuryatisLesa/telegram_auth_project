import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from telegram_auth_project.settings import TELEGRAM_BOT_TOKEN
from .webhook import set_webhook

API_TOKEN = TELEGRAM_BOT_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация маршрутизатора
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await bot.send_message(message.chat.id, 'Привет, сейчас мы тебя зарегистрируем!')

# Функции для работы с базой данных
async def create_db_message(update: types.Update):
    if update.message:
        await bot.send_message(
            update.message.chat.id,
            f"Привет, {update.message.from_user.username}! Ты был добавлен в базу данных."
        )

async def db_message(update: types.Update):
    if update.message:
        await bot.send_message(
            update.message.chat.id,
            f"Привет, {update.message.from_user.username}! Ты уже в базе данных."
        )

async def error_db_message(update: types.Update):
    if update.message:
        await bot.send_message(
            update.message.chat.id,
            "Произошла ошибка при добавлении в базу данных."
        )

# Основная асинхронная функция для запуска бота
async def main():
    # Установка webhook
    set_webhook()

    # Подключение маршрутов
    dp.include_router(router)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Запуск основного процесса
        logging.info('Бот запускается...')
        asyncio.run(main())
        print('Бот запущен')
    except KeyboardInterrupt:
        print('Exit')
        logger.info('Бот остановлен вручную')
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
