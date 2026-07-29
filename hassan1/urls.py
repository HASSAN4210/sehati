from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # الصفحة الرئيسية
    path("", include("catalog.urls")),

    # حسابات المستخدمين
    path("accounts/", include("accounts.urls")),

    # الطلبات
    path("orders/", include("orders.urls")),

    # لوحة التحكم
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )