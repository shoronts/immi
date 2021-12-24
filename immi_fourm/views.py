from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

import json

from .forms import SinglePostForm, EditSinglePost, SearchForm
from .models import ForumPost, ForumComment, AllBookmark

from immi_theme.models import Notification


class ImmiForum:

    # All forums
    def forum(self):
        posts = ForumPost.objects.all().order_by('-post_date')
        if self.method == 'POST' and 'search-topic' in self.POST:
            search = SearchForm(self.POST)
            if search.is_valid():
                search_content = search.cleaned_data['search']
                search_data = ForumPost.objects.filter(title__contains=search_content)
                contex = {
                    'search_content': search_content,
                    'search_data': search_data,
                    'new_post_form': SinglePostForm(),
                    'search': SearchForm()
                }
                return render(self, 'search.html', contex)
            contex = {
                'new_post_form': SinglePostForm(),
                'search': SearchForm(self.POST),
                'notification': Notification.objects.all().order_by('-date').order_by('-date')
            }
        elif self.method == 'POST' and 'new-post' in self.POST:
            post_form = SinglePostForm(self.POST)
            if post_form.is_valid():
                forum_post_author = post_form.save(commit=False)
                forum_post_author.user = self.user
                forum_post_author.save()
                messages.success(self, 'Your post is created.')
                return redirect('forum')
            messages.error(self, 'Something Wrong. Please try again.')
            contex = {
                'posts': posts,
                'new_post_form': post_form,
                'search': SearchForm(),
                'notification': Notification.objects.all().order_by('-date')
            }
        else:
            contex = {
                'search': SearchForm(),
                'posts': posts,
                'new_post_form': SinglePostForm(),
                'notification': Notification.objects.all().order_by('-date').order_by('-date')
            }
        return render(self, 'forum.html', contex)

    # Post Likes
    @login_required
    def user_post_likes(self):
        if self.method == 'POST' and self.is_ajax():
            post_data = json.load(self)
            post_want_to_like = post_data["current_post_id"]
            target_post = get_object_or_404(ForumPost, pk=post_want_to_like)
            if target_post.like.filter(id=self.user.id).exists():
                target_post.like.remove(self.user)
            else:
                target_post.like.add(self.user)
            return JsonResponse({'results': target_post.like.all().count()})

    # User post Comment
    @login_required
    def post_comment(self):
        if self.method == 'POST' and self.is_ajax():
            post_data = json.load(self)
            current_post = get_object_or_404(ForumPost, pk=post_data["current_post_id"])
            main_comments = post_data['comments']
            final_comment = ForumComment(blogs=current_post, person=self.user, comment_body=main_comments)
            final_comment.save()
            data = {'total-comment': current_post.forum_comments.all().count()}
            return JsonResponse(data, safe=False)

    # Comment Likes
    @login_required
    def user_comments_likes(self):
        if self.method == 'POST' and self.is_ajax():
            post_data = json.load(self)
            comment_want_like = post_data["current_comment_id"]
            target_comment = get_object_or_404(ForumComment, pk=comment_want_like)
            if target_comment.all_like.filter(id=self.user.id).exists():
                target_comment.all_like.remove(self.user)
            else:
                target_comment.all_like.add(self.user)
            return JsonResponse({'results': target_comment.all_like.all().count()})
    
    # All Post By User
    @login_required
    def all_post_by_user(self):
        current_post = ForumPost.objects.filter(user=self.user).order_by('-post_date')
        contex = {
            'current_post': current_post,
            'search': SearchForm(),
            'new_post_form': SinglePostForm(),
            'notification': Notification.objects.all().order_by('-date')
        }
        return render(self, 'all-my-post.html', contex)

    # Delete Single Post
    @login_required
    def del_single_post(self, pk):
        delete_data = get_object_or_404(ForumPost, pk=pk)
        if delete_data.user == self.user:
            delete_data.delete()
            messages.success(self, 'Your post is Deleted.')
            return redirect('all-post-user')
        else:
            messages.error(self, 'Your have access only for these posts.')
            return redirect('all-post-user')

    # Edit Single Post
    @login_required
    def edit_single_post(self, pk):
        edit_post = get_object_or_404(ForumPost, pk=pk)
        if edit_post.user == self.user:
            if self.method == 'POST':
                form = EditSinglePost(self.POST)
                if form.is_valid():
                    edit_post.title = form.cleaned_data['title']
                    edit_post.post_description = form.cleaned_data['post_description']
                    edit_post.save()
                    messages.success(self, 'Your post is edited.')
                    return redirect('all-post-user')
                contex = {
                    'form': form,
                    'edit_post': edit_post,
                    'new_post_form': SinglePostForm(),
                    'notification': Notification.objects.all().order_by('-date')
                }
            else:
                contex = {
                    'form': EditSinglePost(),
                    'edit_post': edit_post,
                    'new_post_form': SinglePostForm(),
                    'notification': Notification.objects.all().order_by('-date')
                }
            return render(self, 'edit-single-post.html', contex)
        else:
            messages.error(self, 'Your have access only for these posts.')
            return redirect('all-post-user')

    # Bookmarks Page
    @login_required
    def bookmarks(self):
        if self.method == 'POST' and self.is_ajax():
            post_data_for_bookmarks = json.load(self)
            post_want_to_bookmarks = post_data_for_bookmarks["current_post_id"]
            find_blogs_for_bookmarks = get_object_or_404(ForumPost, pk=post_want_to_bookmarks)
            check_bookmarks = AllBookmark.objects.all()
            for x in check_bookmarks:
                if x.blogs == find_blogs_for_bookmarks and x.user == self.user:
                    x.delete()
                    error_message_done = '<div class="alert alert-danger" role="alert">''<p class="text-center mb-0">' \
                                         'Successfully removed from your bookmarks.</p></div>'
                    return JsonResponse({'results': error_message_done})
            else:
                add_bookmarks = AllBookmark(blogs=find_blogs_for_bookmarks, user=self.user)
                add_bookmarks.save()
                success_message_done = '<div class="alert alert-success" role="alert">' \
                                       '<p class="text-center mb-0">Successfully added to your bookmarks.</p></div>'
                return JsonResponse({'results': success_message_done})
        else:
            contex = {
                'new_post_form': SinglePostForm(),
                'search': SearchForm(),
                'bookmarks': AllBookmark.objects.filter(user=self.user),
                'notification': Notification.objects.all().order_by('-date')
            }
            return render(self, 'bookmarks.html', contex)
