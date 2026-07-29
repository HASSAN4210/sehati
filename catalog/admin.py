from django.contrib import admin

from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    search_fields = (
        "name",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "stock",
        "is_active",
        "is_featured",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "sku",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_editable = (
        "price",
        "stock",
        "is_active",
        "is_featured",
    )

    inlines = [
        ProductImageInline,
    ]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "sort_order",
        "created_at",
    )

    search_fields = (
        "product__name",
    )

    ordering = (
        "sort_order",
    )