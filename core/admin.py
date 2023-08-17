from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django import forms

from .models import User, Profile, Category, Post, Comment, Media


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ["date_joined"]

    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    add_fieldsets = [
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
