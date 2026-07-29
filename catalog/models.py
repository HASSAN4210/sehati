from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="اسم القسم",
    )

    slug = models.SlugField(
        max_length=170,
        unique=True,
        blank=True,
        allow_unicode=True,
        verbose_name="الرابط المختصر",
    )

    description = models.TextField(
        blank=True,
        verbose_name="وصف القسم",
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        verbose_name="صورة القسم",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="القسم نشط",
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
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(
                self.name,
                allow_unicode=True,
            )

            slug = base_slug
            counter = 1

            while Category.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "catalog:category_detail",
            kwargs={"slug": self.slug},
        )


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="القسم",
    )

    name = models.CharField(
        max_length=200,
        verbose_name="اسم المنتج",
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        allow_unicode=True,
        verbose_name="الرابط المختصر",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="رمز المنتج",
    )

    description = models.TextField(
        verbose_name="وصف المنتج",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00"))
        ],
        verbose_name="السعر الأساسي",
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00"))
        ],
        blank=True,
        null=True,
        verbose_name="سعر الخصم",
    )

    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="الكمية المتوفرة",
    )

    main_image = models.ImageField(
        upload_to="products/main/",
        blank=True,
        null=True,
        verbose_name="الصورة الرئيسية",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="متاح للبيع",
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="منتج مميز",
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
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(
                fields=["is_active", "is_featured"]
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(
                self.name,
                allow_unicode=True,
            )

            slug = base_slug
            counter = 1

            while Product.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def current_price(self):
        if self.discount_price is not None:
            return self.discount_price

        return self.price

    @property
    def is_in_stock(self):
        return self.stock > 0

    def get_absolute_url(self):
        return reverse(
            "catalog:product_detail",
            kwargs={"slug": self.slug},
        )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="المنتج",
    )

    image = models.ImageField(
        upload_to="products/gallery/",
        verbose_name="الصورة",
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="وصف الصورة",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتيب الصورة",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة",
    )

    class Meta:
        verbose_name = "صورة منتج"
        verbose_name_plural = "صور المنتجات"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"صورة المنتج: {self.product.name}"