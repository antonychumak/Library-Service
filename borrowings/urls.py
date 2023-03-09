from rest_framework import routers
from django.urls import path, include


from borrowings.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowing", BorrowingViewSet, basename="borrow")


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "borrowing"
