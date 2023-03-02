from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255, verbose_name="Book title")
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
        return self.title

    class Meta:
        ordering = [
            "title",
        ]
