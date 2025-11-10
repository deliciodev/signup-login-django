from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(BaseUserAdmin):
    ordering = ("created_at",)
    list_display = ("email", "username", "name", "id", "is_active", "is_staff", "created_at")
    search_fields = ("email", "username", "name")

    fieldsets = (
        (None, {"fields": ("email", "username", "name", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "name", "password1", "password2"),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        return readonly + ("created_at",)