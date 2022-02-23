from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from blog.models import Blog, Category
from blog.serializers import BlogDetailSerializer, BlogListSerializer, CategoryPaginationSerializer
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView


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


@csrf_exempt
@api_view(['GET'])
def category_pagination(request, **kwargs):
    page = request.GET.get('page', '')
    try:
        category = Category.objects.get(
            slug=kwargs.get('slug')
        )
    except Category.DoesNotExist:
        return Response({
            'ok': False
        })
    blog = Blog.objects.filter(
        is_public=True,
        is_removed=False,
        category=category.id
    )
    blog_paginator = Paginator(blog, 2)
    page_obj = blog_paginator.get_page(page)
    if request.method == 'GET':
        serializer = CategoryPaginationSerializer(
            page_obj,
            many=True
        )
        return render(request, 'index.html', {'data': serializer.data})


class CategoryPagination(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', '')
        try:
            category = Category.objects.get(
                slug=kwargs.get('slug')
            )
        except Category.DoesNotExist:
            return Response({
                'ok': False
            })
        blog = Blog.objects.filter(
            is_public=True,
            is_removed=False,
            category=category.id
        )
        blog_paginator = Paginator(blog, 2)
        page_obj = blog_paginator.get_page(page)
        if self.request.method == 'GET':
            serializer = CategoryPaginationSerializer(
                page_obj,
                many=True
            )
            context['data_list'] = serializer.data
            context['data_title'] = kwargs.get('slug')
        return context
