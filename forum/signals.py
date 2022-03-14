from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from forum.models import Story, Reply
from strgen import StringGenerator as SG

from forum.utils import clean_html


@receiver(pre_save, sender=Story)
def create_story(sender, instance, **kwargs):
    instance.content_safe = clean_html(instance.content)
    if instance._state.adding:
        instance.code = SG(r"[\w]{10}").render()


@receiver(pre_save, sender=Reply)
def create_story(sender, instance, **kwargs):
    instance.content_safe = clean_html(instance.content)
