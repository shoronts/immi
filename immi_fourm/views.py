from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from .forms import single_post_form, edit_single_post
from .models import forum_post, forum_comment


class immu_forum():

    def forum(request):
        posts = forum_post.objects.all().order_by('-post_date')
        return render(request, 'forum/forum.html', {'posts':posts})

    @login_required
    def create_forum_post(request):
        if request.method == 'POST':
            form = single_post_form(request.POST, request.FILES)
            if form.is_valid():
                forum_post_author = form.save(commit=False)
                forum_post_author.user = request.user.username
                forum_post_author.save()
                messages.success(request, 'Your post is created.')
                return redirect('forum')
        else:
            form = single_post_form()
        return render(request, 'forum/create-forum-post.html', {'form':form})

    @login_required
    def every_single_post(request, slug, pk):
        current_post = get_object_or_404(forum_post, pk=pk)

        if request.method == 'POST' and 'like-btn' in request.POST:
            if current_post.like.filter(id=request.user.id).exists():
                current_post.like.remove(request.user)

            else:
                current_post.like.add(request.user)

            return redirect('every-single-post', pk=pk, slug=slug)

        elif request.method == 'POST' and 'comments' in request.POST:
            main_comments = request.POST['user-comments']

            if main_comments:
                final_comment = forum_comment(blogs=current_post, person=request.user, comment_body=main_comments)
                final_comment.save()
                messages.success(request, 'Your comment is posted.')
                return redirect('every-single-post', pk=pk, slug=slug)

            else:
                messages.error(request, 'Empty field not Allowed.')
                return redirect('every-single-post', pk=pk, slug=slug)

        else:
            if current_post.like.filter(id=request.user.id).exists():
                liked = True

            else:
                liked = False

        return render(request, 'forum/every-single-post.html', {'current_post':current_post, 'liked':liked})

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
