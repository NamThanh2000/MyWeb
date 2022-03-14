from django.contrib.auth.models import User
from django.db.models import *
from autoslug import AutoSlugField

class Category(Model):
    name = CharField(max_length=255, unique=True, blank=True)
    slug = AutoSlugField(unique=True, editable=True, blank=True)
    desc_safe = TextField(blank=True)
    order = PositiveSmallIntegerField(default=0)
    color_code = CharField(max_length=10, default='#0a8ddf')


class Story(Model):
    code = CharField(max_length=20, unique=True)
    user = ForeignKey(User, on_delete=PROTECT, related_name='+')
    content = TextField(blank=True)
    content_safe = TextField(blank=True)
    title = CharField(max_length=255, blank=True)
    category = ManyToManyField(Category, related_name='+', blank=True)
    last_activity_by = ForeignKey(User, related_name='+', blank=True, null=True, on_delete=SET_NULL)
    last_activity_at = DateTimeField(auto_now_add=True, editable=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at= DateTimeField(auto_now=True)
    scheduled_at = DateTimeField(blank=True, null=True)
    published_at = DateTimeField(auto_now_add=True, editable=True)
    STORY_STATUS_CHOICES = (
        ('P', 'Công Khai'),
        ('R', 'Đã Xóa'),
        ('S', 'Đang Lên Lịch')
    )
    status = CharField(default='P', db_index=True, max_length=1, choices=STORY_STATUS_CHOICES)
    closed = BooleanField(default=False, db_index=True)
    featured_until = DateTimeField(null=True, blank=True)
    featured = BooleanField()
    edited_at = DateTimeField(blank=True, null=True)
    edited_by = ForeignKey(User, related_name='+', blank=True, null=True, on_delete=SET_NULL)
    num_views = PositiveIntegerField(default=0)
    num_likes = PositiveIntegerField(default=0)
    num_replies = PositiveIntegerField(default=0)
    num_comments = PositiveIntegerField(default=0)
    num_participants = PositiveIntegerField(default=-1)
    ip_address = GenericIPAddressField(blank=True, null=True)
    user_agent = TextField(blank=True)



class Reply(Model):
    user = ForeignKey(User, related_name='+', on_delete=PROTECT)
    story = ForeignKey(Story, related_name='replies', on_delete=CASCADE)
    reply_order = IntegerField()
    content = TextField(blank=True)
    content_safe = TextField(blank=True)
    removed = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    ip_address = GenericIPAddressField(blank=True, null=True)
    user_agent = TextField(blank=True)
    edited_at = DateTimeField(blank=True, null=True)
    edited_by = ForeignKey(User, related_name='+', blank=True, null=True, on_delete=SET_NULL)