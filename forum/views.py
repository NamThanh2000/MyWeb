from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from forum.models import Story, Category, Reply, ReplyComment
from forum.serializers import StorySerializer, CategorySerializer, ReplySerializer, ReplyCommentSerializer, \
    Story_2_Serializer


class CreatePost(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = StorySerializer
    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if not user.is_authenticated:
            return Response({
                'ok': False,
                'msg': 'Chua Dang Nhap'
            })
        if not data:
            return Response({
                'ok': False
            })
        story = Story.objects.create(
            user=user,
            content=data['content'],
            title=data['title'],
        )
        for i in data['category']:
            try:
                category = Category.objects.get(name=i)
            except Category.DoesNotExist:
                return Response({
                    'ok': False
                })
            story.category.add(category)
        return Response({
            'ok': True
        })


class UpdatePost(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = StorySerializer
    def create(self, request, *args, **kwargs):
        data = self.request.data
        storySelector = Story.objects.filter(code=data['code'])
        if not storySelector:
            return Response({
                'ok': False
            })
        storySelector.update(
            content=data['content'],
            title=data['title'],
        )
        for i in data['category']:
            try:
                category = Category.objects.get(id=i)
            except Category.DoesNotExist:
                return Response({
                    'ok': False
                })
            storySelector.first().category.remove()
            storySelector.first().category.add(category)
        return Response({
            'ok': True
        })


class SimpleListPagination(PageNumberPagination):
    page_size = 1
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


class ListUpdatePost(ListAPIView):
    serializer_class = Story_2_Serializer
    permission_classes = [AllowAny]
    pagination_class = SimpleListPagination
    def get_queryset(self):
        story = Story.objects.filter().order_by('-updated_at')
        if not story:
            return Response({
                'ok': False
            })
        objStory = []
        for value in story:
            objCategory = [i.name for i in value.category.all()]
            objStory.append({
                'code': value.code,
                'content': value.content,
                'title': value.title,
                'category': objCategory
            })
        return objStory


class DetailPost(ListAPIView):
    serializer_class = StorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.request.GET.get('slug', '')
        if not slug:
            return []
        story = Story.objects.filter(code=slug)
        if not story:
            return []
        return story


class DeletePost(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = StorySerializer
    def destroy(self, request, *args, **kwargs):
        slug = self.request.GET.get('slug', '')
        if not slug:
            return Response({
            'ok': False
        })
        try:
            Story.objects.get(code=slug).delete()
        except Story.DoesNotExist:
            return Response({
                'ok': False
            })
        return Response({
            'ok': True
        })


class ListReplyPost(ListAPIView):
    serializer_class = ReplySerializer, ReplyCommentSerializer
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs):
        slug = self.request.GET.get('slug', '')
        if not slug:
            return Response({
                'ok': False,
            })
        try:
            story = Story.objects.get(code=slug)
        except Story.DoesNotExist:
            return Response({
                'ok': False,
            })
        try:
            reply = Reply.objects.filter(story=story)
        except Reply.DoesNotExist:
            return Response({
                'ok': False,
            })
        objRE = []
        for i in reply:
            replyComment = ReplyComment.objects.filter(reply=i)
            if not replyComment:
                return Response({
                    'ok': False,
                })
            objRE.append({
                'reply': ReplySerializer(i).data,
                'replyComment': ReplyCommentSerializer(replyComment[:3], many=True).data,
                'totalReply': len(replyComment)
            })
        return Response({
            'ok': True,
            'data': objRE
        })


class OnlyListReplyPost(ListAPIView):
    serializer_class = ReplyCommentSerializer
    permission_classes = [AllowAny]
    pagination_class = SimpleListPagination
    def get_queryset(self):
        id_comment = self.request.GET.get('slug', '')
        if not id_comment:
            return []
        try:
            reply = Reply.objects.get(id=id_comment)
        except Reply.DoesNotExist:
            return []
        replyComment = ReplyComment.objects.filter(reply=reply)
        return replyComment


class CreateReplyPost(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplySerializer
    def create(self, request, *args, **kwargs):
        data = self.request.data
        if not data:
            Response({
                'ok': False
            })
        try:
            user = User.objects.get(id=data['user'])
        except User.DoesNotExist:
            Response({
                'ok': False
            })
        try:
            story = Story.objects.get(id=data['story'])
        except Story.DoesNotExist:
            Response({
                'ok': False
            })
        try:
            edited_by = User.objects.get(id=data['edited_by'])
        except User.DoesNotExist:
            Response({
                'ok': False
            })
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


class UpdateReplyPost(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplySerializer
    def create(self, request, *args, **kwargs):
        idComment = self.request.GET.get('slug', '')
        if not idComment:
            return Response({
                'ok': False
            })
        data = self.request.data
        if not data:
            return Response({
                'ok': False
            })
        try:
            reply = Reply.objects.get(id=idComment)
        except Reply.DoesNotExist:
            return Response({
                'ok': False
            })
        try:
            user = User.objects.get(id=data['user'])
        except User.DoesNotExist:
            return Response({
                'ok': False
            })
        if reply.user == user:
            reply.content = data['content']
            reply.save()
            return Response({
                'ok': True
            })

class DeleteReplyPost(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplySerializer
    def destroy(self, request, *args, **kwargs):
        idComment = self.request.GET.get('slug', '')
        if not idComment:
            return Response({
                'ok': False
            })
        userID = 1
        try:
            _username = User.objects.get(id=userID)
        except User.DoesNotExist:
            return Response({
                'ok': False
            })
        try:
            reply = Reply.objects.get(id=idComment)
        except User.DoesNotExist:
            return Response({
                'ok': False
            })
        if reply.username == _username:
            reply.delete()
        return Response({
            'ok': True
        })


class CreateReplycommentPost(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplyCommentSerializer
    def create(self, request, *args, **kwargs):
        data = self.request.data
        if not data:
            return Response({
                'ok': False
            })
        try:
            user = User.objects.get(id=data['user'])
        except User.DoesNotExist:
            return Response({
                'ok': False
            })
        try:
            reply = Reply.objects.get(id=data['reply'])
        except Reply.DoesNotExist:
            return Response({
                'ok': False
            })
        try:
            mention_to = User.objects.get(id=data['mention_to'])
        except User.DoesNotExist:
            return Response({
                'ok': False
            })
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


class UpdateReplycommentPost(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplyCommentSerializer
    def update(self, request, *args, **kwargs):
        idCommentReply = self.request.GET.get('slug', '')
        if not idCommentReply:
            return Response({
                'ok': False
            })
        data = self.request.data
        if not data:
            return Response({
                'ok': False
            })
        try:
            replycomment = ReplyComment.objects.get(id=idCommentReply)
        except ReplyComment.DoesNotExist:
            return Response({
                'ok': False
            })
        try:
            user = User.objects.get(id=data['user'])
        except ReplyComment.DoesNotExist:
            return Response({
                'ok': False
            })
        if replycomment.user == user:
            replycomment.content = data['content']
            replycomment.save()
            return Response({
                'ok': True
            })


class DeleteReplycommentPost(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReplyCommentSerializer
    def destroy(self, request, *args, **kwargs):
        idComment = self.request.GET.get('slug', '')
        if not idComment:
            return Response({
                'ok': False
            })
        userID = 1
        try:
            username = User.objects.get(id=userID)
        except ReplyComment.DoesNotExist:
            return Response({
                'ok': False
            })
        try:
            replycomment = ReplyComment.objects.get(id=idComment)
        except ReplyComment.DoesNotExist:
            return Response({
                'ok': False
            })
        if replycomment.user == username:
            replycomment.delete()
        return Response({
            'ok': True
        })


class GetCategoryPost(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        category = Category.objects.all()
        arr_category = []
        for i in category:
            arr_category.append(i.name)
        return Response({
            'ok': True,
            'data': arr_category
        })