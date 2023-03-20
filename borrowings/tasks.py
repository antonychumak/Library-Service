from celery import shared_task, Celery

from borrowings.telegram_bot import send_to_telegram


@shared_task()
def test_task():
    print("TEST PRINT")


@shared_task()
def send_feedback_telegram_task(expected_return_date):
    send_to_telegram(
        f"Hurry up! Tomorrow {expected_return_date}"
        f" is your last day to submit your book."
    )
