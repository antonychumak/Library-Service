from datetime import timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs)
        Borrowing.validate_date(
            attrs["borrow_date"],
            attrs["expected_return_date"],
            attrs["actual_return_date"],
            ValidationError,
        )
        return data


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(many=True, read_only=True, slug_field="title")
    user = serializers.ReadOnlyField(source="user.full_name", read_only=True)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=True, read_only=True)
    user_full_name = serializers.ReadOnlyField(source="user.full_name", read_only=True)
    user_email = serializers.ReadOnlyField(source="user.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user_full_name",
            "user_email",
        )
