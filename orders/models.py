from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from catalog.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="المستخدم",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ إنشاء السلة",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    class Meta:
        verbose_name = "سلة تسوق"
        verbose_name_plural = "سلات التسوق"

    def __str__(self):
        return f"سلة المستخدم: {self.user.username}"

    @property
    def total_items(self):
        return sum(
            item.quantity
            for item in self.items.all()
        )

    @property
    def subtotal(self):
        return sum(
            (
                item.total_price
                for item in self.items.select_related(
                    "product"
                )
            ),
            Decimal("0.00"),
        )


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سلة التسوق",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="المنتج",
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ],
        verbose_name="الكمية",
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
        verbose_name = "عنصر سلة"
        verbose_name_plural = "عناصر السلة"

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart",
            ),
        ]

    def __str__(self):
        return (
            f"{self.product.name} × "
            f"{self.quantity}"
        )

    @property
    def unit_price(self):
        return self.product.current_price

    @property
    def total_price(self):
        return self.unit_price * self.quantity


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "قيد المراجعة"
        CONFIRMED = "confirmed", "تم التأكيد"
        PROCESSING = "processing", "قيد التجهيز"
        SHIPPED = "shipped", "تم الشحن"
        DELIVERED = "delivered", "تم التسليم"
        CANCELLED = "cancelled", "ملغي"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "الدفع عند الاستلام"
        CARD = "card", "بطاقة بنكية"
        BANK_TRANSFER = (
            "bank_transfer",
            "تحويل بنكي",
        )

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "بانتظار الدفع"
        PAID = "paid", "مدفوع"
        FAILED = "failed", "فشل الدفع"
        REFUNDED = "refunded", "تم الاسترجاع"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="المستخدم",
    )

    order_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
        verbose_name="رقم الطلب",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        verbose_name="حالة الطلب",
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        verbose_name="طريقة الدفع",
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True,
        verbose_name="حالة الدفع",
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

    shipping_notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات الشحن",
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00"))
        ],
        verbose_name="مجموع المنتجات",
    )

    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00"))
        ],
        verbose_name="تكلفة الشحن",
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00"))
        ],
        verbose_name="قيمة الخصم",
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00"))
        ],
        verbose_name="الإجمالي النهائي",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="تاريخ الطلب",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["order_number"]
            ),
            models.Index(
                fields=["status", "created_at"]
            ),
        ]

    def __str__(self):
        return f"الطلب {self.order_number}"

    def save(self, *args, **kwargs):
        creating = self._state.adding

        if not self.order_number:
            self.order_number = "TEMP"

        self.total = (
            self.subtotal
            + self.shipping_cost
            - self.discount_amount
        )

        if self.total < Decimal("0.00"):
            self.total = Decimal("0.00")

        super().save(*args, **kwargs)

        if creating and self.order_number == "TEMP":
            self.order_number = (
                f"ORD-{self.created_at:%Y%m%d}-"
                f"{self.pk:06d}"
            )

            super().save(
                update_fields=["order_number"]
            )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="الطلب",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
        verbose_name="المنتج",
    )

    product_name = models.CharField(
        max_length=200,
        verbose_name="اسم المنتج",
    )

    product_sku = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="رمز المنتج",
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00"))
        ],
        verbose_name="سعر الوحدة",
    )

    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ],
        verbose_name="الكمية",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة",
    )

    class Meta:
        verbose_name = "عنصر طلب"
        verbose_name_plural = "عناصر الطلب"

    def __str__(self):
        return (
            f"{self.product_name} × "
            f"{self.quantity}"
        )

    @property
    def total_price(self):
        return self.unit_price * self.quantity