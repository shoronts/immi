from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required

from immi_user.models import UserInfo
from immi_theme.models import notification

from .models import users_task, user_task_status


class immi_user_task():

    # Users Task Page
    @login_required
    def task(request):
        all_tasks = users_task.objects.all()
        return render(request, 'dashboard/task.html', {'all_tasks' : all_tasks,'notification': notification.objects.all()})

    # Single Task Page
    @login_required
    def single_task(request, slug):
        single_tasks = get_object_or_404(users_task, task_url=slug)
        if request.method == 'POST' and slug== request.POST['single-task-complete']:
            all_complete_task = user_task_status.objects.all()
            for find_complete_task in all_complete_task:
                if find_complete_task.user == request.user and find_complete_task.task == single_tasks:
                    messages.error(request, 'You have already completed this task.')
                    return redirect('task')
            else:
                task_complete_by = user_task_status(user=request.user, task=single_tasks)
                task_complete_by.save()
                total_task = users_task.objects.all()
                total_completed_task = user_task_status.objects.filter(user=request.user)
                if len(total_task) == len(total_completed_task):
                    change_user_type = UserInfo.objects.get(user=request.user.id)
                    change_user_type.user_type = 'Current Student'
                    change_user_type.save()
                    messages.success(request, 'Now you are a Current Student. Please change your email to the official email.')
                    return redirect('task')
                else:
                    messages.success(request, 'Wellcome! You have completed a task.')
                    return redirect('task')
        return render(request, 'dashboard/single-task.html', {'notification': notification.objects.all().order_by('-date')})
