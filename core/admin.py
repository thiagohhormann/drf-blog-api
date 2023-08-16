from django.contrib import admin

from .models import User, Profile, Category, Post, Comment, Media


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "birthday"]


class PostInline(admin.TabularInline):
    model = Post.category.through
    readonly_fields = ["post"]
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]


class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ["title", "content", "user"]
    extra = 0


class MediaInline(admin.TabularInline):
    model = Media
    readonly_fields = ["file"]
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "categories"]

    inlines = [CommentInline, MediaInline]

    def categories(self, obj):
        return "\n".join([c.name for c in obj.category.all()])


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "post"]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass
