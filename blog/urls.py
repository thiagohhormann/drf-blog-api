from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"profile", views.ProfileViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"posts", views.PostViewSet)
router.register(r"comments", views.CommentViewSet)
router.register(r"medias", views.MediaViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Authentication
    path("api/", include(router.urls)),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),

]
