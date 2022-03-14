from django.contrib import admin

# Register your models here.
from .models import Story, Category, Reply, ReplyComment

# Register your models here.
@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass

@admin.register(ReplyComment)
class ReplyCommentAdmin(admin.ModelAdmin):
    pass