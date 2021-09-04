from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import json

from .forms import single_post_form, edit_single_post, search_form
from .models import forum_post, forum_comment, bookmarks
from immi_theme.models import notification

class immi_forum():

    # All forums
    def forum(request):
        posts = forum_post.objects.all().order_by('-post_date')
        if request.method == 'POST' and 'search-topic' in request.POST:
            search = search_form(request.POST)
            if search.is_valid():
                search_content = search.cleaned_data['search']
                try:
                    search_datas = forum_post.objects.filter(title__contains=search_content)
                except:
                    search_datas = None
                contex = {
                    'search_content':search_content,
                    'search_datas' : search_datas,
                    'new_post_form' : single_post_form(),
                    'search' : search_form()
                }
                return render(request, 'forum/search.html', contex)
            contex = {
                'new_post_form' : single_post_form(),
                'search' : search_form(request.POST),
                'notification': notification.objects.all().order_by('-date').order_by('-date')
            }
        elif request.method == 'POST' and 'new-post' in request.POST:
            post_form = single_post_form(request.POST)
            if post_form.is_valid():
                forum_post_author = post_form.save(commit=False)
                forum_post_author.user = request.user
                forum_post_author.save()
                messages.success(request, 'Your post is created.')
                return redirect('forum')
            messages.error(request, 'Something Wrong. Please try again.')
            contex = {
                'posts': posts,
                'new_post_form' : post_form,
                'search' : search_form(),
                'notification': notification.objects.all().order_by('-date')
            }
        else:
            contex = {
                'search' : search_form(),
                'posts': posts,
                'new_post_form' : single_post_form(),
                'notification': notification.objects.all().order_by('-date').order_by('-date')
            }
        return render(request, 'forum/forum.html', contex)

    # Post Likes
    @login_required
    def user_post_likes(request):
        if request.method == 'POST' and request.is_ajax():
            post_data = json.load(request)
            post_want_to_like = post_data["current_post_id"]
            terget_post = get_object_or_404(forum_post, pk=post_want_to_like)
            if terget_post.like.filter(id=request.user.id).exists():
                terget_post.like.remove(request.user)
            else:
                terget_post.like.add(request.user)
            return JsonResponse({'results':terget_post.like.all().count()})

    # User post Comment
    @login_required
    def post_comment(request):
        if request.method == 'POST' and request.is_ajax():
            post_data = json.load(request)
            current_post = get_object_or_404(forum_post, pk=post_data["current_post_id"])
            main_comments = post_data['comments']
            final_comment = forum_comment(blogs=current_post, person=request.user, comment_body=main_comments)
            final_comment.save()
            data = {'total-comment' : current_post.forum_comments.all().count()}
            return JsonResponse(data, safe=False)

    # Comment Likes
    @login_required
    def user_comments_likes(request):
        if request.method == 'POST' and request.is_ajax():
            post_data = json.load(request)
            comment_want_like = post_data["current_comment_id"]
            terget_comment = get_object_or_404(forum_comment, pk=comment_want_like)
            if terget_comment.all_like.filter(id=request.user.id).exists():
                terget_comment.all_like.remove(request.user)
            else:
                terget_comment.all_like.add(request.user)
            return JsonResponse({'results':terget_comment.all_like.all().count()})
    
    # All Post By User
    @login_required
    def all_post_by_user(request):
        current_post = forum_post.objects.filter(user=request.user).order_by('-post_date')
        contex = {
            'current_post':current_post,
            'search' : search_form(),
            'new_post_form' : single_post_form(),
            'notification': notification.objects.all().order_by('-date')
        }
        return render(request, 'forum/all-my-post.html', contex)

    # Delete Single Post
    @login_required
    def del_single_post(request, slug, pk):
        delete_data = get_object_or_404(forum_post, pk=pk)
        if delete_data.user == request.user:
            delete_data.delete()
            messages.success(request, 'Your post is Deleted.')
            return redirect('all-post-user')
        else:
            messages.error(request, 'Your have access only for these posts.')
            return redirect('all-post-user')

    # Edit Single Post
    @login_required
    def edit_single_post(request, slug, pk):
        edit_post = get_object_or_404(forum_post, pk=pk)
        if edit_post.user == request.user:
            if request.method == 'POST':
                form = edit_single_post(request.POST, request.FILES)
                if form.is_valid():
                    title = form.cleaned_data['title']
                    post_discription = form.cleaned_data['post_discription']
                    try:
                        post_images = request.FILES['post_images']
                        edit_post.post_images = post_images
                    except:
                        pass
                    edit_post.title = title
                    edit_post.post_discription = post_discription
                    edit_post.save()
                    messages.success(request, 'Your post is edited.')
                    return redirect('all-post-user')
            else:
                contex = {
                    'form' : edit_single_post(),
                    'edit_post':edit_post,
                    'new_post_form' : single_post_form(),
                    'notification': notification.objects.all().order_by('-date')
                }
            return render(request, 'forum/edit-single-post.html', contex)
        else:
            messages.error(request, 'Your have access only for these posts.')
            return redirect('all-post-user')

    # Bookmarks Page
    @login_required
    def bookmarks(request):
        if request.method == 'POST' and request.is_ajax():
            post_data_for_bookmarks = json.load(request)
            post_want_to_bookmarks = post_data_for_bookmarks["current_post_id"]
            if bookmarks.objects.filter(blogs=post_want_to_bookmarks).exists():
                remove_bookmarks = get_object_or_404(bookmarks, blogs=post_want_to_bookmarks)
                remove_bookmarks.delete()
                error_message_done = '<div class="alert alert-danger" role="alert"><p class="text-center mb-0">Successfully removed from your bookmarks.</p></div>'
                return JsonResponse({'results':error_message_done})
            else:
                find_blogs_for_bookmarks = get_object_or_404(forum_post, pk=post_want_to_bookmarks)
                add_bookmarks = bookmarks(blogs=find_blogs_for_bookmarks, user=request.user)
                add_bookmarks.save()
                success_message_done = '<div class="alert alert-success" role="alert"><p class="text-center mb-0">Successfully added to your bookmarks.</p></div>'
                return JsonResponse({'results':success_message_done})
        else:
            contex = {
                'new_post_form' : single_post_form(),
                'search' : search_form(),
                'bookmarks' : bookmarks.objects.filter(user=request.user),
                'notification': notification.objects.all().order_by('-date')
            }
        return render(request, 'forum/bookmarks.html', contex)
