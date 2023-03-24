import requests
from django.conf import settings


def send_to_telegram(message_for_user: str) -> None:
    if settings.TELEGRAM_CHAT_ID:
        try:
            requests.post(
                settings.API_URL,
                json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": message_for_user},
            )
        except Exception as e:
            print(f"Oooops....{e}. Try again or contact your administrator")

    print("If you want to use telegram bot, add your TELEGRAM_CHAT_ID to .env according to README.md file")

