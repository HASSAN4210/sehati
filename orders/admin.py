from django.contrib import admin

from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
    )

    inlines = [
        CartItemInline,
    ]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product",
        "quantity",
    )

    search_fields = (
        "product__name",
        "cart__user__username",
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product_name",
        "unit_price",
        "quantity",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "payment_status",
        "total",
        "created_at",
    )

    search_fields = (
        "order_number",
        "user__username",
        "full_name",
    )

    list_filter = (
        "status",
        "payment_status",
        "created_at",
    )

    readonly_fields = (
        "order_number",
        "created_at",
        "updated_at",
    )

    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product_name",
        "quantity",
        "unit_price",
    )

    search_fields = (
        "product_name",
        "order__order_number",
    )