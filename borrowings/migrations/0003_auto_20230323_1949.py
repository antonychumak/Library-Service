from django.core.management import call_command
from django.db import migrations


def fill_borrowings(borrowings, schema_editor):
    call_command("loaddata", "fixture_data.json")


def reverse_func(apps, schema_editor):
    """Should delete instances Borrowings.
    Called when unapplying migrations."""

    Borrowing = apps.get_model("borrowings", "Book")
    db_alias = schema_editor.connection.alias
    Borrowing.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("borrowings", "0002_alter_borrowing_actual_return_date_and_more"),
    ]

    operations = [
        migrations.RunPython(fill_borrowings, reverse_func),
    ]
