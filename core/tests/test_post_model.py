from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Post, Category


class PostModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.category = Category.objects.create(name="Test Category")

        self.post = Post.objects.create(
            title="Test Post Title", content="Test Post Content", user=self.user
        )
        self.post.category.add(self.category)

    def test_post_title(self):
        post = Post.objects.get(id=self.post.id)
        expected_title = "Test Post Title"
        self.assertEqual(post.title, expected_title)

    def test_post_content(self):
        post = Post.objects.get(id=self.post.id)
        expected_content = "Test Post Content"
        self.assertEqual(post.content, expected_content)

    def test_post_user(self):
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.user, self.user)

    def test_post_category(self):
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.category.count(), 1)
        self.assertEqual(post.category.first(), self.category)

    def test_post_date(self):
        post = Post.objects.get(id=self.post.id)
        self.assertIsNotNone(post.date)

    def test_post_string_representation(self):
        post = Post.objects.get(id=self.post.id)
        expected_string = f"Author: {post.user} - ID {post.user_id} | Date: {post.date}"
        self.assertEqual(str(post), expected_string)
