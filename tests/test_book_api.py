from _decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer

BOOK_URL = reverse("books:book-list")


def book_detail_url(book_id: int):
    return reverse("books:book-list", args=[book_id])


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedBookApiTests(TestCase):
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

    def test_book_list(self):
        self.sample_book()

        res = self.client.get(BOOK_URL)

        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_book_forbidden(self):
        payload = {
            "title": "Test Book 2",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 12,
            "daily_fee": 0.99,
        }

        res = self.client.post(BOOK_URL, payload)

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

    def test_create_book(self):
        payload = {
            "title": "Admin Book 7",
            "author": "Admin Author 7",
            "cover": "Hard",
            "inventory": 7,
            "daily_fee": Decimal("0.77"),
        }

        res = self.client.post(BOOK_URL, payload)

        book = Book.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))
