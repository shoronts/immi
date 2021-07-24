from django.urls import path
from .views import immu_theme as theme


urlpatterns = [
    path('', theme.home, name='home'),
    path('search/', theme.search, name='search'),
]
