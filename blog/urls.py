from django.urls import path
from blog import views

urlpatterns = [
    path('blog/', views.blog_list),
    path('blog-detail/', views.blog_detail),
    path('blog-list/', views.blog_list),
]
