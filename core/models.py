from django.db import models
from django.utils import timezone


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    biography = models.CharField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to="core/avatars", blank=True)
    birthday = models.DateField()
    social_media = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def owner(self):
        return self.user_id


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ManyToManyField(Category, related_name="posts")

    def __str__(self):
        return f"Author: {self.user} - ID {self.user_id} | Date: {self.date}"

    @property
    def owner(self):
        return self.user_id


class Comment(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user_id


class Media(models.Model):
    file = models.FileField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.file.name

    @property
    def owner(self):
        return self.user_id
