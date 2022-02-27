from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from blog.models import Blog, Category
from blog.serializers import BlogDetailSerializer, BlogListSerializer, CategoryPaginationSerializer
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.models import User


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
        print(category.id)
        blog = Blog.objects.filter(
            is_public=True,
            is_removed=False,
            category=category.id
        ).order_by('created_at')
        blog_paginator = Paginator(blog, 5)
        page_obj = blog_paginator.get_page(page)
        if self.request.method == 'GET':
            serializer = CategoryPaginationSerializer(
                page_obj,
                many=True
            )
            context['data_list'] = serializer.data
            context['data_title'] = kwargs.get('slug')
            context['page_number'] = page
            context['blog_paginator'] = blog_paginator
            context['link'] = 'http://127.0.0.1:8000/category/' + kwargs.get('slug') + '/?page='
        return context


class BlogPagination(TemplateView):
    template_name = "index_2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', '')
        try:
            _blog = Blog.objects.get(
                slug=kwargs.get('slug')
            )
        except Blog.DoesNotExist:
            return Response({
                'ok': False
            })
        blog = Blog.objects.filter(
            is_public=True,
            is_removed=False,
            category=_blog.category
        ).exclude(id=_blog.id).order_by('created_at')
        blog_paginator = Paginator(blog, 5)
        page_obj = blog_paginator.get_page(page)
        page_count = page_obj.paginator.count/5
        if page_count.is_integer() != True:
            page_count = int(page_obj.paginator.count/5) + 1
        if self.request.method == 'GET':
            serializer = CategoryPaginationSerializer(
                page_obj,
                many=True
            )
            context['data_list'] = serializer.data
            context['data_title'] = _blog.category.slug
            context['page_number'] = page
            context['blog_paginator'] = blog_paginator
            context['page_count'] = range(1, page_count + 1)
            context['link'] = 'http://127.0.0.1:8000/blog/' + kwargs.get('slug') + '/?page='
        return context


@csrf_exempt
@api_view(['GET'])
def blog_api(request, **kwargs):
    if request.method == 'GET':
        blog = Blog.objects.filter(
            is_public=True,
            is_removed=False,
            slug=kwargs.get('slug')
        )
        serializer = BlogListSerializer(
            blog,
            many=True
        )
        return Response({
            'ok': True,
            'data': serializer.data
        })


class LoginPage(LoginView):
    template_name = "index_3.html"


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {'username': UsernameField}


class RegisterPage(FormView):
    template_name = "index_4.html"
    form_class = RegisterForm
    print("nam")

    def form_valid(self, form):
        data = form.cleaned_data
        User.objects.create_user(
            username=data['username'],
            password=data['password1'],
            email=data['email']
        )
        return redirect('/login/')
