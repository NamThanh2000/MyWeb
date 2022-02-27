from django.urls import path
from blog import views


app_name = 'blog'

urlpatterns = [
    path('blog/', views.blog_list),
    path('blog-detail/', views.blog_detail),
    path('blog-list/', views.blog_list),
    path('category/<str:slug>/', views.CategoryPagination.as_view()),
    path('blog/<str:slug>/', views.BlogPagination.as_view()),
    path('api/blog/<str:slug>/', views.blog_api, name="api_blog"),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('profile/', views.ProfilePage.as_view(), name='profile'),
    path('register/', views.RegisterPage.as_view(), name='register'),
]
