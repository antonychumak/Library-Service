from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from borrowings.models import Borrowing
from borrowings.permissions import IsAdminOrIfAuthenticatedReadOnly
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user").prefetch_related("book")
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        return BorrowingSerializer

    def get_queryset(self):
        """Only allow admin or owners of an object to edit it."""

        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user.id)

        return queryset
