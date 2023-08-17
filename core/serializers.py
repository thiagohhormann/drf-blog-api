from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User, Profile, Category, Post, Comment, Media


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
