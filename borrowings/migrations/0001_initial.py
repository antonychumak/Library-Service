# Generated by Django 4.1.7 on 2023-03-02 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("books", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow_date", models.DateField(auto_now_add=True)),
                ("expected_return_date", models.DateField()),
                ("actual_return_date", models.DateField()),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="books.book",
                        verbose_name="books",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="users",
                    ),
                ),
            ],
        ),
    ]
