from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from immi_user.models import UserInfo
from immi_theme.models import Notification

from .models import UserTask, UserTaskStatus


class ImmiUserTask:

    # Users Task Page
    @login_required
    def task(self):
        all_tasks = UserTask.objects.all()
        return render(self, 'dashboard/task.html', {'all_tasks': all_tasks, 'notification': Notification.objects.all()})

    # Single Task Page
    @login_required
    def single_task(self, slug):
        single_tasks = get_object_or_404(UserTask, task_url=slug)
        if self.method == 'POST' and slug == self.POST['single-task-complete']:
            all_complete_task = UserTaskStatus.objects.all()
            for find_complete_task in all_complete_task:
                if find_complete_task.user == self.user and find_complete_task.task == single_tasks:
                    messages.error(self, 'You have already completed this task.')
                    return redirect('task')
            else:
                task_complete_by = UserTaskStatus(user=self.user, task=single_tasks)
                task_complete_by.save()
                total_task = UserTask.objects.all()
                total_completed_task = UserTaskStatus.objects.filter(user=self.user)
                if len(total_task) == len(total_completed_task):
                    change_user_type = UserInfo.objects.get(user=self.user.id)
                    change_user_type.user_type = 'Current Student'
                    change_user_type.save()
                    messages.success(self, 'Now you are a Current Student. Please change your email to the official email.')
                    return redirect('task')
                else:
                    messages.success(self, 'Welcome! You have completed a task.')
                    return redirect('task')
        else:
            contex = {
                'single_task': single_tasks,
                'notification': Notification.objects.all().order_by('-date')
            }
        return render(self, 'dashboard/single-task.html', contex)
