from rest_framework import routers


from borrowings.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowing", BorrowingViewSet, basename="borrow")
print(router.urls)
urlpatterns = router.urls

app_name = "borrowing"
