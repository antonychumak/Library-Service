from django.core.validators import MinValueValidator
from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name="books")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="users")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.book}"
