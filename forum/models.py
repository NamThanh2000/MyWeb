from django.contrib.auth.models import User
from django.db.models import *
from autoslug import AutoSlugField

class Category(Model):
    name = CharField(max_length=255, unique=True, blank=True)
    slug = AutoSlugField(unique=True, editable=True, blank=True)
    desc_safe = TextField(blank=True)
    order = PositiveSmallIntegerField(default=0)
    color_code = CharField(max_length=10, default='#0a8ddf')

