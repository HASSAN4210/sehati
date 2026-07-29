from django.contrib import admin

from .models import Address, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "city",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "phone_number",
    )

    list_filter = (
        "city",
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "city",
        "phone_number",
        "is_default",
    )

    search_fields = (
        "full_name",
        "user__username",
        "phone_number",
        "city",
    )

    list_filter = (
        "city",
        "is_default",
    )

    ordering = (
        "-created_at",
    )