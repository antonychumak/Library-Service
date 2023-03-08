from django.core.validators import MinValueValidator
from django.db import models


from books.models import Book
from library_service import settings
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ManyToManyField(Book, related_name="borrows")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="users"
    )

    def __str__(self):
        return f"{self.actual_return_date} - {self.expected_return_date}"


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
