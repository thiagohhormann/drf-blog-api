from rest_framework import serializers

from .models import User, Profile, Post, Comment, Media, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
