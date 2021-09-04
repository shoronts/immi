from django.urls import path
from .views import immu_message as message


urlpatterns = [
    path('message/', message.message, name='message'),
    path('message/<receiver>/', message.single_message, name='single-message'),
    path('get-all-message-for-client/', message.send_message_to_client, name='get-all-message-for-client'),
    path('group-message/', message.group_message, name='group-message'),
    path('group-message/<slug>/', message.single_group_message, name='single-group-message'),
]
