from django.db.models.signals import post_save, pre_save
from blog.models import Blog, BlogLike
from django.dispatch import receiver
from blog.utils import clean_html


@receiver(post_save, sender=BlogLike)
def create_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.filter(
            id=instance.blog.id
        ).update(total_likes=instance.blog.total_likes + 1)


@receiver(pre_save, sender=Blog)
def update_blog(sender, instance, **kwargs):
    instance.content_safe = clean_html(instance.content)
