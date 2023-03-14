import os
from datetime import datetime
from typing import Type


from django.db import transaction
from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from borrowings.models import Borrowing
from borrowings.permissions import IsAdminOrIfAuthenticatedReadOnly
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer,
    BorrowingDetailSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user").prefetch_related("book")

    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]
    filterset_fields = ["user", "is_active"]

    def get_serializer_class(self) -> Type[Serializer]:
        print("get_serializer_class")
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        print("create View")
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response("Status: Borrow CREATE successfully")

    def perform_create(self, serializer) -> None:
        print("perform_create")
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["POST"],
        url_path="close_borrow",
    )
    def close_borrow(self, request, pk=None):
        print("close_borrow")
        borrow = self.get_object()
        borrow.book.inventory += 1
        borrow.is_active = not borrow.is_active
        serializer = BorrowingSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            borrow.book.save()
            borrow.save()
        return Response("Borrow CLOSE successfully")

    def get_queryset(self) -> QuerySet:
        print("get_queryset")
        """Only allow admin or owners of an object to edit it."""

        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset
