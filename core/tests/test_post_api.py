from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Post, Category


class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        self.posts = []

        self.category1 = Category.objects.create(name="Test Category 1")
        self.category2 = Category.objects.create(name="Test Category 2")

        self.post1 = Post.objects.create(
            title="Post 1", content="Content 1", user=self.user
        )
        self.post1.category.add(self.category1)
        self.posts.append(self.post1)

        self.post2 = Post.objects.create(
            title="Post 2", content="Content 2", user=self.user
        )
        self.post2.category.add(self.category2)
        self.posts.append(self.post2)

        self.post3 = Post.objects.create(
            title="Post 3", content="Content 3", user=self.user
        )
        self.post3.category.add(self.category2)
        self.posts.append(self.post3)

    def test_list_posts(self):
        response = self.client.get("/api/posts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.posts))

        for index, post in enumerate(self.posts):
            self.assertEqual(response.data[index]["title"], post.title)
            self.assertEqual(response.data[index]["content"], post.content)

            self.assertEqual(
                len(response.data[index]["category"]), post.category.count()
            )

            response_category_ids = response.data[index]["category"]
            post_category_ids = post.category.values_list("id", flat=True)

            self.assertListEqual(response_category_ids, list(post_category_ids))


class PostUpdatesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        self.category = Category.objects.create(name="Original Category")

        self.post = Post.objects.create(
            title="Original Post",
            content="Original Content",
            user=self.user,
        )

        self.post.category.add(self.category)

    def get_auth_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_update_post(self):
        token = self.get_auth_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        updated_category = Category.objects.create(name="Update Category")

        update_data = {
            "title": "Update Title",
            "content": "Update Content",
            "category": updated_category.id,
            "user": self.user.id,
        }

        response = self.client.put(f"/api/posts/{self.post.id}/", update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()

        self.assertEqual(self.post.title, update_data["title"])
        self.assertEqual(self.post.content, update_data["content"])
        self.assertEqual(self.post.category.first().id, updated_category.id)

    def test_partial_update_post(self):
        token = self.get_auth_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        partial_update_data = {"title": "Partial Updated Title"}

        response = self.client.patch(f"/api/posts/{self.post.id}/", partial_update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()

        self.assertEqual(self.post.title, partial_update_data["title"])
        self.assertEqual(self.post.category.first().id, self.category.id)


class PostDeleteTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        self.other_user = get_user_model().objects.create_user(
            username="otheruser", email="other@example.com", password="otherpassword"
        )

        self.category = Category.objects.create(name="Test Category")

        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            user=self.user,
        )

        self.post.category.add(self.category)

    def get_auth_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_delete_post(self):
        token = self.get_auth_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"/api/posts/{self.post.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_other_user_post(self):
        token = self.get_auth_token(self.other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"/api/posts/{self.post.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

    def test_delete_post_unauthenticated(self):
        response = self.client.delete(f"/api/posts/{self.post.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
