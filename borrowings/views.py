from django.shortcuts import render
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.permissions import IsAdminOrIfAuthenticatedReadOnly
from borrowings.serializers import BorrowingSerializer


class BorrowingList(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BorrowingDetail(generics.RetrieveUpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
