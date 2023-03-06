from rest_framework import routers
from django.urls import path, include


from borrowings.views import BorrowingList, BorrowingDetail

# router = routers.DefaultRouter()
# router.register("borrowing", BorrowingViewSet)

urlpatterns = [
    path("borrowing/", BorrowingList.as_view()),
    path("borrowing/<int:pk>/", BorrowingDetail.as_view()),
]

app_name = "borrowing"
