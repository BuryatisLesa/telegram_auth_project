from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram import Bot, types
import json
import logging
from django.conf import settings
from .models import CustomUser
from django.db import IntegrityError
from .bot import create_db_message, db_message, error_db_message

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


def telegram_login(request):
    return render(request, 'auth_app_telegram/telegram_login.html')


# Синхронное создание или получение пользователя
def get_or_create_user(telegram_id, username):
    return CustomUser.objects.get_or_create(telegram_id=telegram_id, username=username)


# Асинхронная обработка webhook запросов
@csrf_exempt  # Отключаем CSRF защиту для обработки POST-запросов от Telegram
async def webhook(request):
    if request.method == 'POST':
        try:
            # Получаем данные от Telegram
            json_str = request.body.decode('UTF-8')
            update_data = json.loads(json_str)

            logging.info(f"Получены данные от Telegram: {json_str}")
            username = update_data.get("message", {}).get("from", {}).get("username", None)
            telegram_id = update_data.get("message", {}).get("from", {}).get("id", None)
            update = types.Update(**json.loads(json_str))

            # Обработка пользователя в базе данных
            try:
                user, created = get_or_create_user(telegram_id, username)

                # Если пользователь был создан, отправляем приветственное сообщение
                if created:
                    await create_db_message(update)
                else:
                    await db_message(update)

            except IntegrityError as e:
                # Обработка ошибок уникальности
                logging.error(f"Ошибка при создании пользователя: {e}")
                await error_db_message(update)

            return JsonResponse({"status": "ok"})

        except Exception as e:
            logging.error(f"Ошибка при обработке запроса: {e}")
            return JsonResponse({"error": "Invalid request"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
