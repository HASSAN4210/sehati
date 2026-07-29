from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="المستخدم",
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="رقم الجوال",
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        verbose_name="الصورة الشخصية",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="المدينة",
    )

    address = models.TextField(
        blank=True,
        verbose_name="العنوان",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    class Meta:
        verbose_name = "ملف شخصي"
        verbose_name_plural = "الملفات الشخصية"
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name="المستخدم",
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name="اسم المستلم",
    )

    phone_number = models.CharField(
        max_length=20,
        verbose_name="رقم الجوال",
    )

    city = models.CharField(
        max_length=100,
        verbose_name="المدينة",
    )

    district = models.CharField(
        max_length=100,
        verbose_name="الحي",
    )

    street = models.CharField(
        max_length=150,
        verbose_name="الشارع",
    )

    building_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="رقم المبنى",
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="الرمز البريدي",
    )

    additional_details = models.TextField(
        blank=True,
        verbose_name="تفاصيل إضافية",
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name="العنوان الافتراضي",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    class Meta:
        verbose_name = "عنوان"
        verbose_name_plural = "العناوين"
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.city}"