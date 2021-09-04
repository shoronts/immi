from django.urls import path
from .views import immi_forum as forum


urlpatterns = [
    path('forum/', forum.forum, name='forum'),
    path('likes/', forum.user_post_likes, name='users_likes'),
    path('comment/', forum.post_comment, name='users_comments'),
    path('comment-likes/', forum.user_comments_likes, name='users_comment_likes'),
    path('forum/all-by-me/', forum.all_post_by_user, name='all-post-user'),
    path('forum/edit/<pk>/<slug>/', forum.edit_single_post, name='edit-single-post'),
    path('forum/delete/<pk>/<slug>/', forum.del_single_post, name='delete-single-post'),
    path('forum/bookmarks/', forum.bookmarks, name='bookmarks'),
]
