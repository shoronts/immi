from django.urls import path
from .views import ImmiUserTask


urlpatterns = [
    path('task/', ImmiUserTask.task, name='task'),
    path('task/<slug>/', ImmiUserTask.single_task, name='task-single'),
]