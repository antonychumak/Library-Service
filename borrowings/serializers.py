from rest_framework import serializers

from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title")
    borrows = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "borrows",
        )
