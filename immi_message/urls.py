from django.urls import path
from .views import ImmiMessage


urlpatterns = [
    path('message/', ImmiMessage.message, name='message'),
    path('message/<receiver>/', ImmiMessage.single_message, name='single-message'),
    path('get-all-message-for-client/', ImmiMessage.send_message_to_client, name='get-all-message-for-client'),
    path('group-message/', ImmiMessage.group_message, name='group-message'),
    path('group-message/<slug>/', ImmiMessage.single_group_message, name='single-group-message'),
]
