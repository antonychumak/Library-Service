import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)

BORROW_URL = reverse("borrowings:borrow-list")


def borrow_detail_url(borrow_id: int):
    return reverse("borrowings:borrow-detail", args=[borrow_id])


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@user.com",
            "testpass123",
        )
        self.client.force_authenticate(self.user)

    def sample_book(self, **params):
        defaults = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 12,
            "daily_fee": 2.35,
        }
        defaults.update(params)

        return Book.objects.create(**defaults)

    def sample_borrow(self, **params):
        defaults = {
            "borrow_date": datetime.date.today(),
            "expected_return_date": datetime.date.today(),
            "actual_return_date": datetime.date.today(),
            "book": self.sample_book(**params),
            "user": self.user,
            "is_active": True,
        }
        defaults.update(params)

        return Borrowing.objects.create(**defaults)

    def test_borrowing_list(self):
        self.sample_borrow()

        res = self.client.get(BORROW_URL)

        borrowing = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowing, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_borrowing_detail(self):
        borrowing = self.sample_borrow()

        url = borrow_detail_url(borrowing.id)
        res = self.client.get(url)
        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing_forbidden(self):
        payload = {
            "borrow_date": datetime.date.today(),
            "expected_return_date": datetime.date.today(),
            "actual_return_date": datetime.date.today(),
            "book": self.sample_borrow(),
            "user": self.user,
            "is_active": True,
        }
        res = self.client.post(BORROW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            password="testpass123",
            is_superuser=True,
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

        self.book = Book.objects.create(
            title="Test Book 5",
            author="Test Author 5",
            cover="Hard",
            inventory=10,
            daily_fee=0.99,
        )

    def test_create_borrowing(self):
        payload = {
            "actual_return_date": datetime.date.today(),
            "expected_return_date": datetime.date.today(),
            "book": self.book.id,
            "user": self.user.id,
            "is_active": True,
        }
        res = self.client.post(BORROW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.book.id, 1)
