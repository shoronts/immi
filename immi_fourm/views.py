from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import json

from .forms import single_post_form, edit_single_post, search_form
from .models import forum_post, forum_comment


class immu_forum():

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
                    'search' : search_form()
                }
                return render(request, 'forum/search.html', contex)
            
        else:
            search = search_form()
        return render(request, 'forum/forum.html', {'posts':posts, 'search':search})

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









    @login_required
    def every_single_post(request, slug, pk):
        current_post = get_object_or_404(forum_post, pk=pk)

        if request.method == 'POST' and 'comments' in request.POST:
            main_comments = request.POST['user-comments']

            if main_comments:
                final_comment = forum_comment(blogs=current_post, person=request.user, comment_body=main_comments)
                final_comment.save()
                messages.success(request, 'Your comment is posted.')
                return redirect('every-single-post', pk=pk, slug=slug)

            else:
                messages.error(request, 'Empty field not Allowed.')
                return redirect('every-single-post', pk=pk, slug=slug)

        return render(request, 'forum/every-single-post.html', {'current_post':current_post})
    
    # Create Forums
    @login_required
    def create_forum_post(request):
        if request.method == 'POST':
            form = single_post_form(request.POST, request.FILES)
            if form.is_valid():
                forum_post_author = form.save(commit=False)
                forum_post_author.user = request.user
                forum_post_author.save()
                messages.success(request, 'Your post is created.')
                return redirect('forum')
        else:
            form = single_post_form()
        return render(request, 'forum/create-forum-post.html', {'form':form})

    @login_required
    def all_post_by_user(request):
        current_post = forum_post.objects.all().order_by('-post_date')
        return render(request, 'forum/all-my-post.html', {'current_post':current_post})

    @login_required
    def del_single_post(request, slug, pk):
        delete_data = get_object_or_404(forum_post, pk=pk)
        if delete_data.user == request.user.username:
            delete_data.delete()
            messages.success(request, 'Your post is Deleted.')
            return redirect('all-post-user')
        else:
            messages.error(request, 'Your have access only for these posts.')
            return redirect('all-post-user')

    @login_required
    def edit_single_post(request, slug, pk):
        edit_post = get_object_or_404(forum_post, pk=pk)
        if edit_post.user == request.user.username:
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
                form = edit_single_post()
            return render(request, 'forum/edit-single-post.html', {'edit_post':edit_post, 'form':form})

        else:
            messages.error(request, 'Your have access only for these posts.')
            return redirect('all-post-user')
