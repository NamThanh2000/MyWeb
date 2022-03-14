from rest_framework import serializers
from forum.models import Category, Story, Reply, ReplyComment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'desc_safe',
            'order',
            'color_code'
        ]


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = [
            'user',
            'content',
            'title',
            'category',
            'last_activity_by',
            'scheduled_at',
            'status',
            'closed',
            'featured_until',
            'featured',
            'edited_at',
            'edited_by',
            'num_views',
            'num_likes',
            'num_replies',
            'num_comments',
            'num_participants',
            'ip_address',
            'user_agent'
        ]


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = [
            'user',
            'story',
            'reply_order',
            'content',
            'removed',
            'ip_address',
            'user_agent',
            'edited_at',
            'edited_by'
        ]


class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComment
        fields = [
            'user',
            'reply',
            'content',
            'mention_to',
            'removed',
            'ip_address',
            'user_agent'
        ]

