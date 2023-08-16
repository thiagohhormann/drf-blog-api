from django.db import models


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # add your custom fields here


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    biography = models.CharField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to="core/avatars", blank=True)
    birthday = models.DateField(null=True, blank=True)
    social_media = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    categories = models.ManyToManyField(Category, related_name="posts")

    def __str__(self):
        return f"{self.title} - {self.user} - {self.date}"


class Comment(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Media(models.Model):
    file = models.FileField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
