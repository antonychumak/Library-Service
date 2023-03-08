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
        fourteen_days = timedelta(14)
        day_in_user = attrs["actual_return_date"] - attrs["borrow_date"]
        overdue_days = attrs["actual_return_date"] - attrs["expected_return_date"]
        deadline_date = attrs["borrow_date"] + fourteen_days
        if day_in_user > fourteen_days:
            raise ValidationError(
                f"You cannot borrow a book for more than {fourteen_days} days, deadline: {deadline_date}"
            )
        if attrs["expected_return_date"] > deadline_date:
            raise ValidationError(f"Last day to return book: {deadline_date}")
        if attrs["actual_return_date"] > attrs["expected_return_date"]:
            raise ValidationError(f"You are late with your book for {overdue_days}")

        return attrs


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
