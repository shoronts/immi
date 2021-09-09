from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages

from immi_fourm.forms import SinglePostForm, SearchForm

from .models import SingleMessage, GroupsList, GroupMessage
from .forms import create_group
from immi_theme.models import Notification

import json


class ImmiMessage:
    
    # Message Page
    @login_required
    def message(self):
        contex = {
                'new_post_form': SinglePostForm(),
                'search': SearchForm(),
                'user_list': User.objects.exclude(username=self.user.username).all(),
                'notification': Notification.objects.all().order_by('-date')
            }
        return render(self, 'message/message.html', contex)

    # Single Message Page
    @login_required
    def single_message(self, receiver):
        if self.method == 'POST' and self.is_ajax():
            post_data = json.load(self)
            message_want_to_save = post_data["message"]
            put_message = SingleMessage(sender=self.user.username, receiver=receiver, message=message_want_to_save)
            put_message.save()
            send_message_notification = Notification(
                name='Message Notification',
                user=receiver,
                held_by=self.user.username,
                notification=f"{ self.user.username } send you message - '{ message_want_to_save }'")
            send_message_notification.save()
            return JsonResponse({'results': serializers.serialize("json", SingleMessage.objects.all())})
        else:
            contex = {
                    'new_post_form': SinglePostForm(),
                    'search': SearchForm(),
                    'user_list': User.objects.exclude(username=self.user.username).all(),
                    'current_user_info': get_object_or_404(User, username=receiver),
                    'notification': Notification.objects.all().order_by('-date')
                }
        return render(self, 'message/singlemessage.html', contex)

    # Send All Message
    @login_required
    def send_message_to_client(self):
        if self.method == 'POST' and self.is_ajax():
            return JsonResponse({'results': serializers.serialize("json", SingleMessage.objects.all())})

    # Group Page
    def group_message(self):
        if self.method == 'POST' and 'create-group-request' in self.POST:
            group_form = create_group(self.POST)
            if group_form.is_valid():
                new_group = group_form.cleaned_data['create_group']
                if GroupsList.objects.filter(group_name = new_group).exists():
                    messages.error(self, 'This group is already exists')
                    return redirect('group-message')
                else:
                    create_new_group = GroupsList.objects.create(group_name=new_group)
                    create_new_group.group_member.add(self.user)
                    create_new_group.save()
                    new_group_create_notification = Notification(
                        name='New Group Create Notification',
                        user=self.user.username,
                        held_by=self.user.username,
                        notification=f"Congratulation!! You have successfully created the group '{new_group}'.")
                    new_group_create_notification.save()
                    messages.success(self, 'New Group Created')
                    return redirect('group-message')
            contex = {
                    'new_post_form': SinglePostForm(),
                    'search': create_group(self.POST),
                    'group_form': group_form,
                    'groups_list': GroupsList.objects.all(),
                    'user_list': User.objects.exclude(username=self.user.username).all(),
                    'notification': Notification.objects.all().order_by('-date')
                }
        elif self.method == 'POST' and 'add-group-members' in self.POST:
            new_group_member = self.POST['members']
            terget_group = self.POST['groups']
            find_the_member = get_object_or_404(User, username=new_group_member)
            check_group_status = get_object_or_404(GroupsList, group_name=terget_group)
            if check_group_status.group_member.filter(id=find_the_member.id).exists():
                messages.error(self, 'This member is already added to this group')
                return redirect('group-message')
            else:
                check_group_status.group_member.add(find_the_member.id)
                group_member_added_notification = Notification(
                    name='Group Member Added Notification',
                    user=new_group_member,
                    held_by=self.user.username,
                    notification=f"{ self.user.username } added you to the group '{ terget_group }'")
                group_member_added_notification.save()
                messages.success(self, 'Congratulations. New Group Member Added.')
                return redirect('group-message')
        else:
            contex = {
                    'new_post_form': SinglePostForm(),
                    'search': SearchForm(),
                    'group_form': create_group(),
                    'groups_list': GroupsList.objects.all(),
                    'user_list': User.objects.exclude(username=self.user.username).all(),
                    'notification': Notification.objects.all().order_by('-date')
                }
        return render(self, 'message/groupmessage.html', contex)

    # Group Message
    @login_required
    def single_group_message(self, slug):
        find_group = get_object_or_404(GroupsList, slug=slug)
        if not find_group.group_member.filter(id=self.user.id).exists():
            messages.error(self, 'You are not a member to this group')
            return redirect('group-message')
        elif self.method == 'POST' and self.is_ajax():
            group_message_data = json.load(self)
            group_message_final_data = group_message_data["message"]
            save_group_message = GroupMessage(group=find_group.group_name, sender=self.user.username, message=group_message_final_data)
            save_group_message.save()
            return JsonResponse({'results': serializers.serialize("json", GroupMessage.objects.filter(group=find_group.group_name))})
        elif self.method == 'GET' and self.is_ajax():
            return JsonResponse({'results': serializers.serialize("json", GroupMessage.objects.filter(group=find_group.group_name))})
        else:
            contex = {
                    'new_post_form': SinglePostForm(),
                    'search': SearchForm(),
                    'groups_list': GroupsList.objects.all(),
                    'current_groups_info': find_group,
                    'notification': Notification.objects.all().order_by('-date')
                }
        return render(self, 'message/groupmessagebox.html', contex)
