from django.db import migrations
from django.core.management import call_command


def fill_books(books, schema_editor):
    call_command("loaddata", "fixture_data.json")


def reverse_func(apps, schema_editor):
    """Should delete instances Book.
    Called when unapplying migrations."""

    Book = apps.get_model("book", "Book")
    db_alias = schema_editor.connection.alias
    Book.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(fill_books, reverse_func),
    ]
