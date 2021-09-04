from django.urls import path
from .views import immu_theme as theme


urlpatterns = [
    path('', theme.home, name='home'),
    path('accommodation/', theme.accommodation, name='accommodation'),
    path('immigration/', theme.immigration, name='immigration'),
    path('covid-info/', theme.covid_info, name='covid-info'),
    path('notifications/', theme.notifications, name='notifications'),
]
