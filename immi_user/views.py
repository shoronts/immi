from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib.auth import update_session_auth_hash

from .token import account_activation_token, password_reset_token, email_change_token
from .forms import loginForm, RegisterForm, PassResetEmailForm, PassResteForm, passChangeForm, profile_change_form
from .models import UserInfo

from immi_theme.models import Notification


class ImmiUserAuth:

    # Users Registration Page
    def register(self):
        if self.user.is_authenticated:
            return redirect('home')
        elif self.method == 'POST':
            form = RegisterForm(self.POST)
            if form.is_valid():
                first_name = form.cleaned_data['firstName']
                last_name = form.cleaned_data['lastName']
                email = form.cleaned_data['email']
                user_name = form.cleaned_data['userName']
                password = form.cleaned_data['password']
                nationality = form.cleaned_data['nationality']
                program = form.cleaned_data['program']
                if '@umail.ucc.ie' in email:
                    user_type = 'Current Student'
                else:
                    user_type = 'Prospective Student'
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                username=user_name, password=password)
                user.is_active = False
                user.save()
                users_info = UserInfo(user=user, user_type=user_type, nationality=nationality, program=program)
                users_info.save()
                current_site = get_current_site(self)
                email_subject = f"Account Activation Link for {current_site.domain}"
                final_email = render_to_string('activeaccount/activate.html', {
                        'user': first_name,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user)
                    })
                email_message = strip_tags(final_email)
                main_email = EmailMultiAlternatives(
                        email_subject,
                        email_message,
                        settings.EMAIL_HOST_USER,
                        [email],
                    )
                main_email.attach_alternative(final_email, "text/html")
                main_email.send()
                create_account_notification = Notification(
                    name='Create Account Notification',
                    user=user_name,
                    held_by=user_name,
                    notification=f"Congratulations!! You have successfully Signup")
                create_account_notification.save()
                messages.success(self, "Your account is created successfully. Please check your email "
                                          "and activate your account. Otherwise you can't access "
                                          "our services. Thank you!")
                return redirect('register')
        else:
            form = RegisterForm()
        return render(self, 'users/register.html', {'form':form})

    # Users Account Activation Page
    def activate_account_view(self, uidb64, token):
        if self.user.is_authenticated:
            return redirect('home')
        else:
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and account_activation_token.check_token(user, token) or \
                    user is not None and email_change_token.check_token(user, token):
                user.is_active = True
                user.save()
                activate_account_notification = Notification(
                    name='Account Activate Notification',
                    user=user.username,
                    held_by=user.username,
                    notification=f"Congratulations!! You account is activated")
                activate_account_notification.save()
                return render(self, 'activeaccount/activate_success.html')
            elif not account_activation_token.check_token(user, token) or \
                    not email_change_token.check_token(user, token):
                return render(self, 'activeaccount/account_already_active.html')
            else:
                return render(self, 'activeaccount/activate_failed.html')

    # Users Login Page
    def login(self):
        if self.user.is_authenticated:
            return redirect('home')
        elif self.method == 'POST':
            form = loginForm(self.POST)
            if form.is_valid():
                username = form.cleaned_data['userName']
                password = form.cleaned_data['password']
                if User.objects.get(username=username).is_active:
                    user = auth.authenticate(self, username=username, password=password)
                    if user is not None:
                        auth.login(self, user)
                        if 'next' in self.POST:
                            return redirect(self.POST.get('next'))
                        else:
                            return redirect('home')
                else:
                    messages.error(self, 'Please verify your email first.')
                    return redirect('login')
        else:
            form = loginForm()
        return render(self, 'users/login.html', {'form' : form})

    # Users Profile Page
    @login_required
    def profile(self):
        if self.method == 'POST':
            form = profile_change_form(self.POST, self.FILES)
            if form.is_valid():
                first_name = form.cleaned_data['firstName']
                last_name = form.cleaned_data['lastName']
                email = form.cleaned_data['email']
                try:
                    profile_pic = self.FILES['profile_pic']
                    user_profile_update = UserInfo.objects.get(user=self.user.id)
                    user_profile_update.profilepic = profile_pic
                    user_profile_update.save()
                except:
                    pass
                if email != self.user.email:
                    user_mainprofile_update = User.objects.get(pk=self.user.id)
                    user_mainprofile_update.first_name = first_name
                    user_mainprofile_update.last_name = last_name
                    user_mainprofile_update.email = email
                    user_mainprofile_update.is_active = False
                    user_mainprofile_update.save()
                    current_site = get_current_site(self)
                    user = User.objects.get(pk=self.user.id)
                    email_subject = f"Email Activation Link for {current_site.domain}"
                    final_email = render_to_string('activeaccount/email_change_email.html', {
                            'user': self.user.first_name,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': email_change_token.make_token(user)
                        })
                    email_message = strip_tags(final_email)
                    main_email = EmailMultiAlternatives(
                            email_subject,
                            email_message,
                            settings.EMAIL_HOST_USER,
                            [email],
                        )
                    main_email.attach_alternative(final_email, "text/html")
                    main_email.send()
                    messages.success(self, 'Please check your email.')
                    return redirect('login')
                else:
                    user_mainprofile_update = User.objects.get(pk=self.user.id)
                    user_mainprofile_update.first_name = first_name
                    user_mainprofile_update.last_name = last_name
                    user_mainprofile_update.email = email
                    user_mainprofile_update.save()
                    messages.success(self, 'Your profile is updated')
                    return redirect('profile')
        else:
            form = profile_change_form()
        return render(self, 'users/profile.html', {'form': form,
                                                   'notification': Notification.objects.all().order_by('-date')})

    # # Users Password Change Page
    @login_required
    def change_password(self):
        if self.method == 'POST':
            form = passChangeForm(user=self.user, data=self.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(self, self.user)
                messages.success(self, 'Congratulation!! Your password was successfully updated!')
                return redirect('change_password')
        else:
            form = passChangeForm(user=self.user)
        return render(self, 'recoveraccount/changepassword.html',
                      {'form': form, 'notification': Notification.objects.all().order_by('-date')})

    # Users Logout Page
    def logout(self):
        if self.user.is_authenticated:
            auth.logout(self)
        return redirect('login')

    # Users Reset Password Email Sending Page
    def password_reset_email(self):
        if self.user.is_authenticated:
            return redirect('home')
        elif self.method == 'POST':
            form = PassResetEmailForm(self.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user = User.objects.get(email=email)
                user.is_active = False
                user.save()
                current_site = get_current_site(self)
                email_subject = f"Password Reset Link for {current_site.domain}"
                finalemail = render_to_string('recoveraccount/resetemail.html',
                            {'user': user.first_name,
                            'username' : user.username,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': password_reset_token.make_token(user)})
                email_message = strip_tags(finalemail)
                reset_main_email = EmailMultiAlternatives(
                        email_subject,
                        email_message,
                        settings.EMAIL_HOST_USER,
                        [email],
                    )
                reset_main_email.attach_alternative(finalemail, "text/html")
                reset_main_email.send()
                messages.success(self, 'An email with the password reset instructions is send to your givan email. '
                                       'Please check your email and follow the instructions. Thank you!!')
                return redirect('passReste')
        else:
            form = PassResetEmailForm()
        return render(self, 'recoveraccount/resetform.html', {'form' : form})

    # Users Reset Password Email Confirmation Page
    def password_reset_form(self, uidb64, token):
        if self.user.is_authenticated:
            return redirect('home')
        elif self.method == 'POST':
            form = PassResteForm(self.POST)
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if form.is_valid():
                if user is not None and password_reset_token.check_token(user, token):
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.is_active = True
                    user.save()
                    messages.success(self, 'Your Password has been set successfully.')
                    return redirect('login')
                else:
                    messages.error(self, 'This link is invalid. Please self a new one.')
                    return redirect('passReste')
        else:
            form = PassResteForm()
        return render(self, 'recoveraccount/resetconfirm.html',
                      {'form': form, 'uidb': uidb64, 'token': token})
