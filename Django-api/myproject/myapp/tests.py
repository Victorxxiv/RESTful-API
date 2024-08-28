from django.test import TestCase
from rest_framework.test import APIClient
from .models import Post

# Create your tests here
class PostTestCase(TestCase):
    def setUP(self):
        self.Client = APIClient()
        self.post = Post.objects.create(title="Test Post", content="Test content", author="Tester")

        def test_post_creation(self):
            response = self.client.post('/api/posts/', {'title': 'New Post', 'content': 'New Content', 'author': 'Tester'})
            self.assertEqual(response.status_code, 201)