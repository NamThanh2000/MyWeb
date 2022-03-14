from django.urls import path
from blog import views


app_name = 'blog'

urlpatterns = [
    path('blog/', views.blog, name="blog_main"),
    path('api/blog-list/', views.blog_list, name="api_blog_list"),
    path('api/blog-detail/', views.blog_detail, name="api_blog_detail"),
    path('api/blog-detail-list/', views.BlogDetailList.as_view(), name="api_blog_detail_list"),
    path('blog-list/', views.blog_list, name="blog_list"),
    path('category/<str:slug>/', views.CategoryPagination.as_view(), name="category"),
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
    path('api/blogformpost/', views.get_blog_form_post_api_view, name="api_blog_form_post"),
    path('blogformedit/', views.blog_form_view_edit.as_view(), name="blog_form_edit"),
    path('api/blogformedit/', views.get_blog_form_edit_api_view, name="api_blog_form_edit"),
    path('api/blogformeditpost/', views.get_blog_form_edit_post_api_view, name="api_blog_form_edit_post"),
]
