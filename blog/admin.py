from django.contrib import admin

# Register your models here.
from .models import Blog, Category, BlogLike

admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(BlogLike)