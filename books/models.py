from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255, unique=True, verbose_name="Book title")
    author = models.CharField(max_length=50, verbose_name="Author")
    cover = models.CharField(max_length=50, choices=CoverChoices.choices)
    inventory = models.PositiveIntegerField(verbose_name="Availability of books")
    daily_fee = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=4,
        decimal_places=2,
        verbose_name="Daily fee",
    )

    def __str__(self) -> str:
        return f"{self.title} | Availability of books: {self.inventory}"

    @staticmethod
    def validate_inventory(inventory: int, error_to_raise):
        if inventory <= 0:
            raise error_to_raise("This book is not currently available.")

    def clean(self):
        Book.validate_inventory(self.inventory, ValidationError)

    class Meta:
        ordering = [
            "title",
        ]
        unique_together = ("title", "author")
