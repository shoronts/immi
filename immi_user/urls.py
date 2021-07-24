from django.urls import path
from .views import UsersView as users


urlpatterns = [
    path('register/', users.register, name='register'),
    path('activate/<uidb64>/<token>', users.ActivateAccountView, name='activateaccount' ),
    path('profile/', users.profile, name='profile'),
    path('login/', users.login, name='login'),
    path('logout/', users.logout, name='logout'),
    path('password-reset/', users.PasswordResetEmail, name='passReste'),
    path('password-reset-confirm/<uidb64>/<token>/', users.PasswordResetForm , name='password_reset_confirm'),
    path('change-password/', users.change_password, name='change_password'),
]
