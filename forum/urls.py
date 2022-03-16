from django.urls import path
from forum import views


app_name = 'forum'

urlpatterns = [
    path('api/create-post', views.create_post.as_view(), name="create_post"),
    path('api/update-post', views.update_post.as_view(), name="update_post"),
]
