from django.urls import path
from blog import views


app_name = 'blog'

urlpatterns = [
    path('', views.blog),
    path('blog/', views.blog_list),
    path('blog-detail/', views.blog_detail),
    path('blog-list/', views.blog_list),
    path('category/<str:slug>/', views.CategoryPagination.as_view()),
    path('blog/<str:slug>/', views.BlogPagination.as_view(), name="blog"),
    path('api/blog/<str:slug>/', views.blog_api, name="api_blog"),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('profile/', views.ProfilePage.as_view(), name='profile'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('logout/', views.LogOutPage, name='logout'),
    path('api/bloglike/', views.get_blog_like_api_view, name="api_like"),
    path('api/bloglikepost/', views.get_blog_like_post_api_view, name="api_like_post"),
    path('blogform/', views.blog_form_view.as_view(), name="blog_form"),
    path('api/blogform/', views.get_blog_form_api_view, name="api_blog_form"),
    path('api/blogformpost/', views.get_blog_form_post_api_view, name="api_blog_form_post")
]
