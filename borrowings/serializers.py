from datetime import timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    inventory_book = serializers.ReadOnlyField(source="book.inventory", read_only=True)
    borrow_date = serializers.DateField(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
            "user",
            "inventory_book",
            "is_active",
        )

    def validate(self, attrs: dict) -> dict:
        data = super(BorrowingSerializer, self).validate(attrs)
        Borrowing.validate_date(
            attrs["expected_return_date"],
            ValidationError,
        )
        if attrs["book"].inventory <= 0:
            raise ValidationError({"Book inventory is empty"})
        return data

    def create(self, validated_data: dict) -> dict:
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        return super().create(validated_data)


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(many=False, read_only=True, slug_field="title")
    user = serializers.ReadOnlyField(source="user.full_name", read_only=True)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user_full_name = serializers.ReadOnlyField(source="user.full_name", read_only=True)
    user_email = serializers.ReadOnlyField(source="user.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
            "user_full_name",
            "user_email",
            "inventory_book",
            "is_active",
        )
