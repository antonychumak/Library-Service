from rest_framework import routers
from django.urls import path, include

from books.views import BookViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet, basename="book")

urlpatterns = router.urls

app_name = "books"
