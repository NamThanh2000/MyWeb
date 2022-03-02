from django.db.models.signals import post_save
from blog.models import Blog, BlogLike
from django.dispatch import receiver

@receiver(post_save, sender=BlogLike)
def create_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.filter(
            id=instance.blog.id
        ).update(total_likes=instance.blog.total_likes + 1)
