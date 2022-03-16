from django.urls import path
from forum import views


app_name = 'forum'

urlpatterns = [
    path('api/create-post/', views.create_post.as_view(), name="create_post"),
    path('api/update-post/', views.update_post.as_view(), name="update_post"),
    path('api/list-update-post/', views.list_update_post.as_view(), name="list_update_post"),
    path('api/detail-post/', views.detail_post.as_view(), name="detail_post"),
]
