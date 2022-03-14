
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from forum.models import Story, Category
from forum.serializers import StorySerializer, CategorySerializer


class create_post(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = StorySerializer
    def create(self, request, *args, **kwargs):
        data = self.request.data
        user = User.objects.get(id=data['user'])
        last_activity_by = User.objects.get(id=data['last_activity_by'])
        edited_by = User.objects.get(id=data['edited_by'])
        category = Category.objects.get(id=data['category'])
        story = Story.objects.create(
            user=user,
            content=data['content'],
            title=data['title'],
            last_activity_by=last_activity_by,
            scheduled_at=data['scheduled_at'],
            status=data['status'],
            closed=data['closed'],
            featured_until=data['featured_until'],
            featured=data['featured'],
            edited_at=data['edited_at'],
            edited_by=edited_by,
            num_views=data['num_views'],
            num_likes=data['num_likes'],
            num_replies=data['num_replies'],
            num_comments=data['num_comments'],
            num_participants=data['num_participants'],
            ip_address=data['ip_address'],
            user_agent=data['user_agent'],
        )
        story.category.add(category)
        return Response({
            'ok': True
        })
