from django.urls import path
from forum import views


app_name = 'forum'

urlpatterns = [
    path('api/create-post/', views.create_post.as_view(), name="create_post"),
    path('api/update-post/', views.update_post.as_view(), name="update_post"),
    path('api/list-update-post/', views.list_update_post.as_view(), name="list_update_post"),
    path('api/detail-post/', views.detail_post.as_view(), name="detail_post"),
    path('api/delete-post/', views.delete_post.as_view(), name="delete_post"),
    path('api/list-reply-post/', views.list_reply_post.as_view(), name="list_reply_post"),
    path('api/only_list-reply-post/', views.only_list_reply_post.as_view(), name="only_list_reply_post"),
    path('api/create-reply-post/', views.create_reply_post.as_view(), name="create_reply_post"),
    path('api/update-reply-post/', views.update_reply_post.as_view(), name="update_reply_post"),
    path('api/delete-reply-post/', views.delete_reply_post.as_view(), name="delete_reply_post"),
    path('api/create-replycomment-post/', views.create_replycomment_post.as_view(), name="create_replycomment_post"),
    path('api/update-replycomment-post/', views.update_replycomment_post.as_view(), name="update_replycomment_post"),
    path('api/delete-replycomment-post/', views.delete_replycomment_post.as_view(), name="delete_replycomment_post"),
    path('test/', views.test.as_view(), name="test")
]
