from django.urls import path
from forum import views


app_name = 'forum'

urlpatterns = [
    path('api/create-post/', views.CreatePost.as_view(), name="create_post"),
    path('api/update-post/', views.UpdatePost.as_view(), name="update_post"),
    path('api/list-update-post/', views.ListUpdatePost.as_view(), name="list_update_post"),
    path('api/detail-post/', views.DetailPost.as_view(), name="detail_post"),
    path('api/delete-post/', views.DeletePost.as_view(), name="delete_post"),
    path('api/list-reply-post/', views.ListReplyPost.as_view(), name="list_reply_post"),
    path('api/only_list-reply-post/', views.OnlyListReplyPost.as_view(), name="only_list_reply_post"),
    path('api/create-reply-post/', views.CreateReplyPost.as_view(), name="create_reply_post"),
    path('api/update-reply-post/', views.UpdateReplyPost.as_view(), name="update_reply_post"),
    path('api/delete-reply-post/', views.DeleteReplyPost.as_view(), name="delete_reply_post"),
    path('api/create-replycomment-post/', views.CreateReplycommentPost.as_view(), name="create_replycomment_post"),
    path('api/update-replycomment-post/', views.UpdateReplycommentPost.as_view(), name="update_replycomment_post"),
    path('api/delete-replycomment-post/', views.DeleteReplycommentPost.as_view(), name="delete_replycomment_post"),
    path('api/get-category-post/', views.GetCategoryPost.as_view(), name="get_category_post"),
]
