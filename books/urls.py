from rest_framework import routers
from django.urls import path, include

from books.views import BookViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "books"