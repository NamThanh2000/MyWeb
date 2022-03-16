from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
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


class update_post(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = StorySerializer
    def create(self, request, *args, **kwargs):
        data = self.request.data
        storySelector = Story.objects.filter(code=data['code'])
        storySelector.update(
            content=data['content'],
            title=data['title'],
        )
        for i in data['category']:
            category = Category.objects.get(id=i)
            storySelector.first().category.remove()
            storySelector.first().category.add(category)
        return Response({
            'ok': True
        })

class SimpleListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'numItems': self.page.paginator.count,
            'totalPages': self.page.paginator.num_pages,
            'pageSize': self.page_size,
            'currentPage': self.page.number,
            'items': data,
        })

class list_update_post(ListAPIView):
    serializer_class = StorySerializer
    permission_classes = [AllowAny]
    pagination_class = SimpleListPagination
    def get_queryset(self):
        story = Story.objects.filter().order_by('-updated_at')
        return story


class detail_post(ListAPIView):
    serializer_class = StorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.request.GET.get('slug', '')
        story = Story.objects.filter(code=slug)
        return story


class delete_post(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = StorySerializer
    def destroy(self, request, *args, **kwargs):
        slug = self.request.GET.get('slug', '')
        Story.objects.get(code=slug).delete()
        return Response({
            'ok': True
        })