import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


from books.models import Book
from library_service import settings
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="users"
    )

    def __str__(self):
        return f"{self.actual_return_date} - {self.expected_return_date}"

    @staticmethod
    def validate_date(expected_return_date, actual_return_date, error_to_raise):
        borrow_date = datetime.date.today()
        fourteen_days = timedelta(14)
        day_in_user = actual_return_date - borrow_date
        overdue_days = actual_return_date - expected_return_date
        deadline_date = borrow_date + fourteen_days
        if day_in_user > fourteen_days:
            raise error_to_raise(
                f"You cannot borrow a book for more than {fourteen_days} days, deadline: {deadline_date}"
            )
        if expected_return_date > deadline_date:
            raise error_to_raise(f"Last day to return book: {deadline_date}")
        if actual_return_date > expected_return_date:
            raise error_to_raise(f"You are late with your book for {overdue_days}")
        if actual_return_date < borrow_date:
            raise error_to_raise(f"return date is incorrect")

    def clean(self):
        Borrowing.validate_date(
            self.borrow_date,
            self.expected_return_date,
            self.actual_return_date,
            ValidationError,
        )

    class Meta:
        ordering = ("id",)


class Payment:
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        PAID = "PAID"

    class TapeChoices(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    session_url = models.URLField
    session = models.CharField()
    money_to_pay = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=4,
        decimal_places=2,
        verbose_name="Money to pay",
    )
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "borrowing"
