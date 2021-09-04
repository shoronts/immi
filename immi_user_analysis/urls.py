from django.urls import path
from .views import immi_user_task as dashboard


urlpatterns = [
    path('task/', dashboard.task, name='task'),
    path('task/<slug>/', dashboard.single_task, name='task-single'),
]