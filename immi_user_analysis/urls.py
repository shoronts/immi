from django.urls import path
from .views import DashboardView as dashboard


urlpatterns = [
    path('task/', dashboard.task, name='task'),
    path('task/<slug>/', dashboard.single_task, name='task-single'),
    path('accommodation/', dashboard.accommodation, name='accommodation'),
    path('immigration/', dashboard.immigration, name='immigration'),
]