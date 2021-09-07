from django.urls import path
from .views import ImmiUserAuth


urlpatterns = [
    path('register/', ImmiUserAuth.register, name='register'),
    path('activate/<uidb64>/<token>', ImmiUserAuth.activate_account_view, name='activateaccount'),
    path('profile/', ImmiUserAuth.profile, name='profile'),
    path('login/', ImmiUserAuth.login, name='login'),
    path('logout/', ImmiUserAuth.logout, name='logout'),
    path('password-reset/', ImmiUserAuth.password_reset_email, name='passReste'),
    path('password-reset-confirm/<uidb64>/<token>/', ImmiUserAuth.password_reset_form, name='password_reset_confirm'),
    path('change-password/', ImmiUserAuth.change_password, name='change_password'),
]
