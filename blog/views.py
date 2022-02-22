from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from blog.models import Blog
from blog.serializers import BlogDetailSerializer, BlogListSerializer


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def blog_list(request):
    if request.method == 'GET':
        blog = Blog.objects.filter(
            is_public=True,
            is_removed=False,
        )[:10]
        serializer = BlogListSerializer(
            blog,
            many=True
        )
        return Response({
            'ok': True,
            'data': serializer.data
        })

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BlogListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'ok': True,
                'data': serializer.data
            })
        return Response({
            'ok': False
        })


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request):
    slug = request.GET.get('slug', '')
    try:
        blog = Blog.objects.get(
            is_public=True,
            is_removed=False,
            slug=slug
        )
    except Blog.DoesNotExist:
        return Response({
            'ok': False
        })

    if request.method == 'GET':
        serializer = BlogDetailSerializer(blog)
        return Response({
            'ok': True,
            'data': serializer.data
        })

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BlogDetailSerializer(
            blog,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'ok': True,
                'data': serializer.data
            })
        return Response({
            'ok': False
        })

    elif request.method == 'DELETE':
        blog.delete()
        return HttpResponse(status=204)
