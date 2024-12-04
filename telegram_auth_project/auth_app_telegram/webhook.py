import requests
from django.conf import settings
import logging

def set_webhook():
    # Устанавливаем URL для webhook, с использованием вашего ngrok URL
    webhook_url = f"https://c338-95-191-1-178.ngrok-free.app/webhook/"  # Обязательно добавьте /webhook в конце URL
    telegram_api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}"

    try:
        # Отправляем запрос на установку webhook
        response = requests.get(telegram_api_url)
        
        # Проверяем успешный статус ответа
        if response.status_code == 200:
            print("Webhook successfully set.")
            logging.info("Webhook successfully set.")
        else:
            # Логируем ошибку, если установка не удалась
            print(f"Error setting webhook: {response.status_code}")
            logging.error(f"Error setting webhook: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        # Обрабатываем возможные исключения при запросе
        print(f"Error making request to Telegram API: {e}")
        logging.error(f"Error making request to Telegram API: {e}")
