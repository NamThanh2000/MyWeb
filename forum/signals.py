from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from forum.models import Story
from strgen import StringGenerator as SG


@receiver(pre_save, sender=Story)
def create_story(sender, instance, **kwargs):
    if instance._state.adding:
        instance.code = SG(r"[\w]{10}").render()
