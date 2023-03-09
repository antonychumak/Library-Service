from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

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
    filterset_fields = ["user"]

    def create(self, request: Request, *args: tuple, **kwargs: dict):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({"Order created successfully"})

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    def get_queryset(self):
        """Only allow admin or owners of an object to edit it."""

        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
