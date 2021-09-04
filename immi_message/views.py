from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages

from immi_fourm.forms import single_post_form, search_form

from .models import single_message, groups_list, group_message
from .forms import create_group
from immi_theme.models import notification

import json


class immu_message():
    
    # Message Page
    @login_required
    def message(request):
        contex = {
                'new_post_form' : single_post_form(),
                'search' : search_form(),
                'user_list' : User.objects.exclude(username=request.user.username).all(),
                'notification': notification.objects.all().order_by('-date')
            }
        return render(request, 'message/message.html', contex)

    # Single Message Page
    @login_required
    def single_message(request, receiver):
        if request.method == 'POST' and request.is_ajax():
            post_data = json.load(request)
            message_want_to_save = post_data["message"]
            put_message = single_message(sender=request.user.username, receiver=receiver, message=message_want_to_save)
            put_message.save()
            send_message_notification = notification(
                name = 'Message Notification',
                user = receiver,
                held_by = request.user.username,
                notification = f"{ request.user.username } send you message - '{ message_want_to_save }'")
            send_message_notification.save()
            return JsonResponse({'results':serializers.serialize("json", single_message.objects.all())})
        else:
            contex = {
                    'new_post_form' : single_post_form(),
                    'search' : search_form(),
                    'user_list' : User.objects.exclude(username=request.user.username).all(),
                    'current_user_info' : get_object_or_404(User, username=receiver),
                    'notification': notification.objects.all().order_by('-date')
                }
        return render(request, 'message/singlemessage.html', contex)

    # Send All Message
    @login_required
    def send_message_to_client(request):
        if request.method == 'POST' and request.is_ajax():
            return JsonResponse({'results':serializers.serialize("json", single_message.objects.all())})

    # Group Page
    def group_message(request):
        if request.method == 'POST' and 'create-group-request' in request.POST:
            group_form = create_group(request.POST)
            if group_form.is_valid():
                new_group = group_form.cleaned_data['create_group']
                if groups_list.objects.filter(group_name = new_group).exists():
                    messages.error(request, 'This group is already exists')
                    return redirect('group-message')
                else:
                    create_new_group = groups_list.objects.create(group_name=new_group)
                    create_new_group.group_member.add(request.user)
                    create_new_group.save()
                    new_group_create_notification = notification(
                        name = 'New Group Create Notification',
                        user = request.user.username,
                        held_by = request.user.username,
                        notification = f"Congratulatuion!! You have successfully created the group '{new_group}'.")
                    new_group_create_notification.save()
                    messages.success(request, 'New Group Created')
                    return redirect('group-message')
            contex = {
                    'new_post_form' : single_post_form(),
                    'search' : search_form(),
                    'group_form' : group_form,
                    'groups_list' : groups_list.objects.all(),
                    'user_list' : User.objects.exclude(username=request.user.username).all(),
                    'notification': notification.objects.all().order_by('-date')
                }
        elif request.method == 'POST' and 'add-group-members' in request.POST:
            new_group_member = request.POST['members']
            terget_group = request.POST['groups']
            find_the_member = get_object_or_404(User,username=new_group_member)
            check_group_status = get_object_or_404(groups_list, group_name=terget_group)
            if check_group_status.group_member.filter(id=find_the_member.id).exists():
                messages.error(request, 'This member is already added to this group')
                return redirect('group-message')
            else:
                check_group_status.group_member.add(find_the_member.id)
                group_member_added_notification = notification(
                    name = 'Group Member Added Notification',
                    user = new_group_member,
                    held_by = request.user.username,
                    notification = f"{ request.user.username } added you to the group '{ terget_group }'")
                group_member_added_notification.save()
                messages.success(request, 'Congratulations. New Group Member Added.')
                return redirect('group-message')
            contex = {
                    'new_post_form' : single_post_form(),
                    'search' : search_form(),
                    'group_form' : group_form,
                    'groups_list' : groups_list.objects.all(),
                    'user_list' : User.objects.exclude(username=request.user.username).all(),
                    'notification': notification.objects.all().order_by('-date')
                }
        else:
            contex = {
                    'new_post_form' : single_post_form(),
                    'search' : search_form(),
                    'group_form' : create_group(),
                    'groups_list' : groups_list.objects.all(),
                    'user_list' : User.objects.exclude(username=request.user.username).all(),
                    'notification': notification.objects.all().order_by('-date')
                }
        return render(request,'message/groupmessage.html', contex)

    # Group Message
    @login_required
    def single_group_message(request, slug):
        find_group = get_object_or_404(groups_list, slug=slug)
        if not find_group.group_member.filter(id=request.user.id).exists():
            messages.error(request, 'You are not a member to this group')
            return redirect('group-message')
        elif request.method == 'POST' and request.is_ajax():
            group_message_data = json.load(request)
            group_message_final_data = group_message_data["message"]
            save_group_message = group_message(group=find_group.group_name, sender=request.user.username, message=group_message_final_data)
            save_group_message.save()
            return JsonResponse({'results':serializers.serialize("json", group_message.objects.filter(group=find_group.group_name))})
        elif request.method == 'GET' and request.is_ajax():
            return JsonResponse({'results':serializers.serialize("json", group_message.objects.filter(group=find_group.group_name))})
        else:
            contex = {
                    'new_post_form' : single_post_form(),
                    'search' : search_form(),
                    'groups_list' : groups_list.objects.all(),
                    'current_groups_info' : find_group,
                    'notification': notification.objects.all().order_by('-date')
                }
        return render(request,'message/groupmessagebox.html', contex)
