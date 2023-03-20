import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models

from books.models import Book
from borrowings.tasks import send_feedback_telegram_task
from library_service import settings
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now=True)
    expected_return_date = models.DateField(
        default=datetime.date.today() + timedelta(14)
    )
    actual_return_date = models.DateField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="users"
    )
    is_active = models.BooleanField(default=False)
    borrow_cost = models.DecimalField(
        decimal_places=2, max_digits=4, null=True, blank=True
    )

    def __str__(self):
        return f"{self.borrow_date} - {self.expected_return_date}"

    @staticmethod
    def validate(actual_return_date, is_active, error_to_raise) -> None:
        borrow_date = datetime.date.today()
        fourteen_days = timedelta(14)
        if actual_return_date:
            day_in_user = actual_return_date - borrow_date
            if day_in_user > fourteen_days:
                raise error_to_raise("Your borrowings overdue")
        if not is_active:
            raise error_to_raise("Your borrowing already close")

    def clean(self):
        Borrowing.validate(
            self.actual_return_date,
            self.is_active,
            ValidationError,
        )

    def send_warning(self):
        if self.is_active:
            send_feedback_telegram_task.delay(self.expected_return_date)

    class Meta:
        ordering = ("id",)
