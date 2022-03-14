from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from blog.models import Blog, Category, BlogLike
from blog.serializers import BlogDetailSerializer, BlogListSerializer, CategoryPaginationSerializer, BlogLikeSerializer
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.models import User
from lxml.html.clean import Cleaner


@csrf_exempt
@api_view(['GET'])
def blog(request):
    blog = Blog.objects.filter(
        is_public=True,
        is_removed=False,
    )
    serializer = BlogListSerializer(
        blog,
        many=True
    )
    return render(request, 'main.html', {'data_list': serializer.data})


@csrf_exempt
@api_view(['GET'])
def blog_list(request):
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


@csrf_exempt
@api_view(['GET'])
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
    return Response({
        'ok': True,
        'data': {
            'username': blog.user.username,
            'created_at': blog.created_at,
            'total_likes': blog.total_likes,
            'content': blog.content_safe,
            'title': blog.title
        }
    })


class BlogDetailList(ListAPIView):
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        slug = self.request.GET.get('slug', '')
        if not slug:
            return []
        _blog = Blog.objects.filter(
            slug=slug
        ).only('id', 'category_id').first()
        if not _blog:
            return []
        blog = Blog.objects.select_related('category').filter(
            is_public=True,
            is_removed=False,
            category_id=_blog.category_id
        ).exclude(id=_blog.id).order_by('-created_at')
        return blog


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


class BlogPagination(LoginRequiredMixin, TemplateView):
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
        page_count = page_obj.paginator.count / 5
        if page_count.is_integer() != True:
            page_count = int(page_obj.paginator.count / 5) + 1
        if self.request.method == 'GET':
            serializer = CategoryPaginationSerializer(
                page_obj,
                many=True
            )

            context['data_list'] = serializer.data
            context['blog'] = _blog
            context['data_title'] = _blog.category.slug
            context['page_number'] = page
            context['blog_paginator'] = blog_paginator
            context['page_count'] = range(1, page_count + 1)
            context['slug'] = kwargs.get('slug')
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

    def form_valid(self, form):
        data = form.cleaned_data
        User.objects.create_user(
            username=data['username'],
            password=data['password1'],
            email=data['email']
        )
        return redirect('/login/')


def LogOutPage(request):
    logout(request)
    return redirect("/login/")


@csrf_exempt
@api_view(['GET'])
def get_blog_like_api_view(request, **kwargs):
    _user = request.user
    slug = request.GET.get('slug')
    if not slug:
        return Response({
            'ok': False
        })
    if not _user.is_authenticated:
        return Response({
            'ok': False
        })
    blog = Blog.objects.filter(
        is_public=True,
        is_removed=False,
        slug=slug
    ).first()
    if BlogLike.objects.filter(
            user=_user,
            blog=blog
    ).exists():
        check_like = True
    else:
        check_like = False
    return Response({
        'ok': True,
        'data': {
            'isLiked': check_like,
            'totalLike': blog.total_likes,
        }
    })


@csrf_exempt
@api_view(['POST'])
def get_blog_like_post_api_view(request, **kwargs):
    slug = request.data.get('slug')
    _user = request.user
    if not slug:
        return Response({
            'ok': False
        })
    if not _user.is_authenticated:
        return Response({
            'ok': False
        })
    blog = Blog.objects.filter(
        is_public=True,
        is_removed=False,
        slug=slug
    ).only('id').first()
    if not blog:
        return Response({
            'ok': False
        })
    BlogLike.objects.create(user=_user, blog=blog)
    return Response({
        'ok': True
    })


@csrf_exempt
@api_view(['GET'])
def get_blog_form_api_view(request, **kwargs):
    _user = request.user
    if not _user.is_authenticated:
        return Response({
            'ok': False
        })
    cate = Category.objects.values_list('name', flat=True)
    return Response({
        'ok': True,
        'data': {
            'cate': cate
        }
    })


@csrf_exempt
@api_view(['POST'])
def get_blog_form_post_api_view(request, **kwargs):
    _user = request.user
    if not _user.is_authenticated:
        return Response({
            'ok': False
        })
    cate = Category.objects.get(name=request.data['category'])
    print(request.data)
    slug_newest = Blog.objects.create(title=request.data['title'], content=request.data['content'], category=cate,
                                      is_public=True, user=_user)
    return Response({
        'slug': slug_newest.slug,
        'ok': True
    })


class blog_form_view(TemplateView):
    template_name = "blog_form.html"


@csrf_exempt
@api_view(['GET'])
def get_blog_form_edit_api_view(request, **kwargs):
    _user = request.user
    slug = request.GET.get('slug')
    if not _user.is_authenticated:
        return Response({
            'ok': False
        })
    cate = Category.objects.values_list('name', flat=True)
    blog = Blog.objects.filter(slug=slug).first()
    if (blog.user == _user):
        return Response({
            'ok': True,
            'data': {
                'cate': cate,
                'blog': {
                    'title': blog.title,
                    'content': blog.content,
                    'category': blog.category.name
                }
            }
        })
    return Response({
        'ok': False
    })


@csrf_exempt
@api_view(['POST'])
def get_blog_form_edit_post_api_view(request, **kwargs):
    _user = request.user
    if not _user.is_authenticated:
        return Response({
            'ok': False
        })
    _blog = Blog.objects.filter(slug=request.data['slug']).first()
    if not _blog:
        return Response({
            'ok': False
        })
    cate = Category.objects.get(name=request.data['category'])
    _blog.title = request.data['title']
    _blog.content = request.data['content']
    _blog.category = cate
    _blog.save()
    return Response({
        'slug': _blog.slug,
        'ok': True
    })


class blog_form_view_edit(TemplateView):
    template_name = "blog_form_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['slug'] = self.request.GET.get('slug')
        return context
