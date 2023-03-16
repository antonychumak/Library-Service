import requests
from django.conf import settings


def send_to_telegram(message_for_user):
    try:
        requests.post(
            settings.API_URL,
            json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": message_for_user},
        )
    except Exception as e:
        print(f"Oooops....{e}")
