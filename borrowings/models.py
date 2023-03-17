import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models


from books.models import Book
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
    def validate(actual_return_date, error_to_raise) -> None:
        borrow_date = datetime.date.today()
        fourteen_days = timedelta(14)
        if actual_return_date:
            day_in_user = actual_return_date - borrow_date
            if day_in_user > fourteen_days:
                raise error_to_raise("Your borrowings overdue")

    @staticmethod
    def validate_is_active(is_active, error_to_raise) -> None:
        print("VALIDATION IN MODEL")
        if not is_active:
            raise error_to_raise("Your borrowing already close")

    def clean(self):
        Borrowing.validate(
            self.actual_return_date,
            ValidationError,
        )

    # def borrowing_cost(self):
    #     if self.actual_return_date == self.borrow_date:
    #         cost_borrow = self.book.daily_fee
    #     else:
    #         days_in_borrow = self.actual_return_date - self.borrow_date
    #         print(days_in_borrow)
    #         cost_borrow = days_in_borrow.days * self.book.daily_fee
    #         print(cost_borrow)
    #     return cost_borrow

    class Meta:
        ordering = ("id",)
