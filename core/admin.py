from django.contrib import admin

from .models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Registration",
            {
                "fields": [
                    "username",
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                ],
            },
        ),
        (
            "Permissions",
            {
                "fields": ["is_superuser", "is_staff", "groups"],
            },
        ),
        ("Status", {"fields": ["is_active"]}),
    ]

    list_display = ["username", "email", "first_name", "last_name", "is_active"]


admin.site.register(Profile)
