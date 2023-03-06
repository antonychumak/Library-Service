from django.contrib.auth import get_user_model
from rest_framework import serializers

from borrowings.models import Borrowing
from books.serializers import BookSerializer
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book_title = serializers.CharField(source="book.title")
    borrows = serializers.ReadOnlyField(source="user.full_name")

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_title",
            "borrows",
        )


class BorrowDetailSerializer(BorrowingSerializer):
    borrows = serializers.ReadOnlyField(source="user.full_name")
