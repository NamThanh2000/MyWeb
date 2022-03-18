from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from forum.models import Story, Category, Reply, ReplyComment
from forum.serializers import StorySerializer, CategorySerializer, ReplySerializer, ReplyCommentSerializer


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


class list_reply_post(ListAPIView):
    serializer_class = ReplySerializer, ReplyCommentSerializer
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs):
        slug = self.request.GET.get('slug', '')
        story = Story.objects.get(code=slug)
        reply = Reply.objects.filter(story=story)
        objRE = []
        for i in reply:
            replyComment = ReplyComment.objects.filter(reply=i)
            objRE.append({
                'reply': ReplySerializer(i).data,
                'replyComment': ReplyCommentSerializer(replyComment[:3], many=True).data,
                'totalReply': len(replyComment)
            })
        return Response({
            'ok': True,
            'data': objRE
        })


class only_list_reply_post(ListAPIView):
    serializer_class = ReplyCommentSerializer
    permission_classes = [AllowAny]
    pagination_class = SimpleListPagination
    def get_queryset(self):
        id_comment = self.request.GET.get('slug', '')
        reply = Reply.objects.get(id=id_comment)
        replyComment = ReplyComment.objects.filter(reply=reply)
        return replyComment


class create_reply_post(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplySerializer
    def create(self, request, *args, **kwargs):
        data = self.request.data
        user = User.objects.get(id=data['user'])
        story = Story.objects.get(id=data['story'])
        edited_by = User.objects.get(id=data['edited_by'])
        Reply.objects.create(
            user=user,
            story=story,
            reply_order=data['reply_order'],
            content=data['content'],
            removed=data['removed'],
            ip_address=data['ip_address'],
            user_agent=data['user_agent'],
            edited_at=data['edited_at'],
            edited_by=edited_by,
        )
        return Response({
            'ok': True
        })


class update_reply_post(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplySerializer
    def create(self, request, *args, **kwargs):
        idComment = self.request.GET.get('slug', '')
        data = self.request.data
        reply = Reply.objects.get(id=idComment)
        user = User.objects.get(id=data['user'])
        if reply.user == user:
            reply.content = data['content']
            reply.save()
            return Response({
                'ok': True
            })

class delete_reply_post(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplySerializer
    def destroy(self, request, *args, **kwargs):
        idComment = self.request.GET.get('slug', '')
        userID = 1
        _username = User.objects.get(id=userID)
        reply = Reply.objects.get(id=idComment)
        if reply.username == _username:
            reply.delete()


class create_replycomment_post(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplyCommentSerializer
    def create(self, request, *args, **kwargs):
        data = self.request.data
        user = User.objects.get(id=data['user'])
        reply = Reply.objects.get(id=data['reply'])
        mention_to = User.objects.get(id=data['mention_to'])
        ReplyComment.objects.create(
            user=user,
            reply=reply,
            content=data['content'],
            mention_to=mention_to,
            removed=data['removed'],
            ip_address=data['ip_address'],
            user_agent=data['user_agent']
        )
        return Response({
            'ok': True
        })


class test(ListAPIView):
    serializer_class = ReplyCommentSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        replyComment = ReplyComment.objects.filter(id=1)
        return replyComment