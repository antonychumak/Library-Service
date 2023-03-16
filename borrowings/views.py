import asyncio
import os
from datetime import datetime
from typing import Type


from django.db import transaction
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiParameter
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
from borrowings.telegram_bot import send_to_telegram


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user").prefetch_related("book")

    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]
    filterset_fields = ["user", "is_active"]

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def get_queryset(self) -> QuerySet:
        """Only allow admin or owners of an object to edit it."""

        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    @action(
        detail=True,
        methods=["POST"],
        url_path="close_borrow",
    )
    def close_borrow(self, request, pk=None):
        """Endpoint for closing a borrow"""

        borrow = self.get_object()
        borrow.book.inventory += 1
        borrow.is_active = not borrow.is_active
        serializer = BorrowingSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            borrow.book.save()
            borrow.save()
            (
                send_to_telegram(
                    f"Congratulations {borrow.user.first_name} "
                    f"you closed the borrowing of the book {borrow.book}"
                    f" today {borrow.actual_return_date}"
                )
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                description="Filter by is_active field",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="user_id",
                description="Filter by user_id",
                required=False,
                type=int,
            ),
        ]
    )
    def list(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().list(request, *args, **kwargs)
