from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'medias', views.MediaViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls))
]
