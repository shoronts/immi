from django.urls import path
from .views import ImmiTheme


urlpatterns = [
    path('', ImmiTheme.home, name='home'),
    path('accommodation/', ImmiTheme.accommodation, name='accommodation'),
    path('immigration/', ImmiTheme.immigration, name='immigration'),
    path('covid-info/', ImmiTheme.covid_info, name='covid-info'),
    path('notifications/', ImmiTheme.notifications, name='notifications'),
]
