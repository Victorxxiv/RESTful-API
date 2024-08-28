from rest_framework import serializers
from .models import Post

# Create a serializer class
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"