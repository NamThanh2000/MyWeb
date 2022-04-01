from .models import Blog
from haystack import indexes

class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    username = indexes.CharField(model_attr='user__username')
    created_at = indexes.DateTimeField(model_attr='created_at')
    # updated_at = indexes.DateTimeField(model_attr='first_name')
    is_public = indexes.BooleanField(model_attr='is_public')
    is_removed = indexes.BooleanField(model_attr='is_removed')
    total_likes = indexes.IntegerField(model_attr='total_likes')

    def get_model(self):
        return Blog

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_removed=False, is_public=True)