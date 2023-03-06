from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/library/", include("books.urls", namespace="books")),
    path("api/users/", include("users.urls", namespace="users")),
    path("api/order/", include("borrowings.urls", namespace="borrowings")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
