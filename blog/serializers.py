from rest_framework import serializers
from blog.models import Blog


class BlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'created_at', 'updated_at', 'is_public', 'is_removed']


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'created_at', 'updated_at']
