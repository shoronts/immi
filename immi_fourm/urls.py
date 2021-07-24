from django.urls import path
from .views import immu_forum as forum


urlpatterns = [
    path('all-forum/', forum.forum, name='forum'),
    path('forum/create-post/', forum.create_forum_post, name='create-forum-post'),
    path('forum/edit/<pk>/<slug>/', forum.edit_single_post, name='edit-single-post'),
    path('forum/delete/<pk>/<slug>/', forum.del_single_post, name='delete-single-post'),
    path('forum/all-by-me/', forum.all_post_by_user, name='all-post-user'),
    path('forum/<pk>/<slug>/', forum.every_single_post, name='every-single-post'),
]
