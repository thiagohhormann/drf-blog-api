from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Post, Category


class PostViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.category = Category.objects.create(name="Test Category")
        self.post = Post.objects.create(
            title="Test Post Title", content="Test Post Content", user=self.user
        )
        self.post.category.add(self.category)

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_list_posts(self):
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = {
            "title": "Updated Post Title",
            "content": "Updated Post Content",
            "category": [self.category.id],
            "user": self.user.id,
        }
        response = self.client.put(f"/api/posts/{self.post.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = {"title": "Partial Updated Title"}
        response = self.client.patch(f"/api/posts/{self.post.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.delete(f"/api/posts/{self.post.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
