from rest_framework import serializers
from forum.models import Category, Story, Reply, ReplyComment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'slug',
            'name',
            'desc_safe',
            'order',
            'color_code'
        ]


class UserSerializer(serializers.Serializer):
    username=serializers.CharField()
    avatar_url=serializers.CharField()

    def get_avatar_url(self):
        return f'https://ui-avatars.com/api/?name={self.username}'


class StorySerializer(serializers.ModelSerializer):
    category=CategorySerializer(many=True)
    last_activity_by=UserSerializer()
    edited_by=UserSerializer()
    class Meta:
        model = Story
        fields = [
            'user',
            'content',
            'content_safe',
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


class Story_3_Serializer(serializers.Serializer):
    # class Meta:
    #     model = Story
    #     fields = [
    #         'pk'
    #         'content',
    #         'title',
    #         'category'
    #     ]
    title = serializers.CharField()
    content = serializers.CharField()
    category = CategorySerializer(many=True)


class Story_2_Serializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj['category']