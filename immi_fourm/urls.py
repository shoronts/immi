from django.urls import path
from .views import ImmiForum


urlpatterns = [
    path('forum/', ImmiForum.forum, name='forum'),
    path('likes/', ImmiForum.user_post_likes, name='users_likes'),
    path('comment/', ImmiForum.post_comment, name='users_comments'),
    path('comment-likes/', ImmiForum.user_comments_likes, name='users_comment_likes'),
    path('forum/all-by-me/', ImmiForum.all_post_by_user, name='all-post-user'),
    path('forum/edit/<pk>/', ImmiForum.edit_single_post, name='edit-single-post'),
    path('forum/delete/<pk>/', ImmiForum.del_single_post, name='delete-single-post'),
    path('forum/bookmarks/', ImmiForum.bookmarks, name='bookmarks'),
]
