from django.contrib.auth.models import User
from django.db import models
from autoslug import AutoSlugField


class Blog(models.Model):
    title = models.CharField(max_length=200, null=True)
    slug = AutoSlugField(max_length=255, unique=True, populate_from='title', editable=True, blank=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    total_likes = models.IntegerField(blank=True, null=True, default=0)


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(blank=True, null=True)


class BlogLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
