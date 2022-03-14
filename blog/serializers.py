from rest_framework import serializers
from blog.models import Blog, Category, BlogLike


class BlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'created_at', 'updated_at', 'is_public', 'is_removed', 'user']


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'created_at', 'updated_at', 'slug']


class CategoryPaginationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'created_at', 'updated_at', 'slug']


class BlogLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogLike
        fields = ['user', 'blog']
