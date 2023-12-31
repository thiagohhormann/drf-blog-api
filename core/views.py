from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

from .models import Profile, User, Category, Post, Comment, Media
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    CategorySerializer,
    PostSerializer,
    CommentSerializer,
    MediaSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticatedOrReadOnly]
        if self.action in ["update", "partial_update", "destroy"]:
            permission_classes.append(IsOwnerOrReadOnly)
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticatedOrReadOnly]
        if self.action in ["update", "partial_update", "destroy"]:
            permission_classes.append(IsOwnerOrReadOnly)
        return [permission() for permission in permission_classes]


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
