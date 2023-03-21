from celery import shared_task

from borrowings.telegram_bot import send_to_telegram


@shared_task()
def send_feedback_telegram_task() -> None:
    send_to_telegram(f"Hurry up! Tomorrow is your last day to submit your book.")
