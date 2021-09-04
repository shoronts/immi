from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.hashers import check_password


# Login Form
class loginForm(forms.Form):
    userName = forms.CharField(label = "Your Username",
        error_messages = {'required' : 'Username required.'},
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'placeholder' : 'Your Username',
                'class' : 'form-control'
                }
            )
        )

    password = forms.CharField(label = "Your Password",
        min_length = 8,
        max_length = 50,
        error_messages = {'required' : 'Password required.'},
        widget = forms.PasswordInput(
            attrs = { 
                'placeholder' : 'Your Password',
                'class' : 'form-control'
                }
            )
        )

    
    def clean_userName(self):
        data = self.cleaned_data['userName']
        if not User.objects.filter(username = data).exists():
            raise ValidationError("Username Doesn't Match")
        return data

    def clean(self):
        cleaned_data = super().clean()
        login_password = cleaned_data.get("password")
        
        if login_password:
            username = cleaned_data.get("userName")
            try:
                users_current_password = User.objects.filter(username = username).first()

                if not check_password(login_password, users_current_password.password):
                    self.add_error('password', "Wrong Password. Please try again!!!")
            except:
                pass


# Registeration Form
class RegisterForm(forms.Form):

    firstName = forms.CharField(label = "First Name",
            error_messages = {'required' : 'First Name Required.'},
            max_length = 100,
            widget = forms.TextInput(
                attrs = {
                    'placeholder' : 'First Name',
                    'class' : 'form-control'
                }
                )
            )
        
    lastName = forms.CharField(label = "Last Name",
        error_messages = {'required' : 'Last Name Required.'},
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'placeholder' : 'Last Name',
                'class' : 'form-control'
                }
            )
        )

    userName = forms.CharField(label = "Username",
        error_messages = {'required' : 'Username Required.'},
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'placeholder' : 'Username',
                    'class' : 'form-control'}
            )
        )

    email = forms.EmailField(label = "Email",
        help_text = 'Please use a valid Email.',
        error_messages = {'required' : 'Valid Email Required.'},
        max_length = 100,
        widget = forms.EmailInput(
            attrs = {
                'placeholder' : 'Email',
                    'class' : 'form-control'}
            )
        )

    password = forms.CharField(label = "Password",
        error_messages = {'required' : 'Strong Password Required.'},
        min_length = 8,
        help_text = 'Minimum 8 Characters..',
        max_length = 50,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder' : 'Password',
                    'class' : 'form-control'}
            )
        )

    confirmPassword = forms.CharField(label = "Confirm Your Password",
        error_messages = {'required' : 'Strong Password Required.'},
        min_length = 8,
        help_text = 'Minimum 8 Characters..',
        max_length = 50,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder' : 'Confirm Password',
                    'class' : 'form-control'}
            )
        )

    nationality = forms.CharField(label = "What’s your nationality",
        error_messages = {'required' : 'nationality Required.'},
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'placeholder' : 'nationality',
                    'class' : 'form-control'}
            )
        )

    program = forms.CharField(label = "What’s your Program ",
        error_messages = {'required' : 'program Required.'},
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'placeholder' : 'program',
                    'class' : 'form-control'}
            )
        )

    def clean_userName(self):
        data = self.cleaned_data['userName']
        if User.objects.filter(username = data).exists():
            raise ValidationError("A user with this username already exists!")
        return data
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email = data).exists():
            raise ValidationError("A user with this Email already exists!")
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmPassword = cleaned_data.get("confirmPassword")

        if password and confirmPassword and password != confirmPassword:
                error = "Password Did not Match!!"
                self.add_error('password', error)
                self.add_error('confirmPassword', error)


# Password Reset Email Form
class PassResetEmailForm(PasswordResetForm):
    email = forms.EmailField(required= True,label='Email',
            widget=forms.EmailInput(attrs={
                    'placeholder':'Enter a valid email',
                    'class' : 'form-control'
                }),
            error_messages={'required': 'Enter A Valid Email.'},
        )
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if not User.objects.filter(email = data).exists():
            raise ValidationError("This Email dosen't exists!")
        return data


# Password Reset Email Confirmation Form
class PassResteForm(forms.Form):
    password = forms.CharField(required=True, label='New Password',
                    widget=forms.PasswordInput(attrs={
                        'placeholder' : 'New Password',
                        'class' : 'form-control'
                      }),
                    error_messages={'required': 'New Password Required.'},
                    min_length=8,
                    max_length=50)
    confirmPassword = forms.CharField(required=True, label='Confirm Password',
                    widget=forms.PasswordInput(attrs={
                        'placeholder' : 'Confirm Password',
                         'class' : 'form-control'
                      }),
                    error_messages={'required': 'Confirm Password Required.'},
                    min_length=8,
                    max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmPassword = cleaned_data.get("confirmPassword")

        if password and confirmPassword:
            if password != confirmPassword:
                error = "Password Did not Match!!"
                self.add_error('password', error)
                self.add_error('confirmPassword', error)


# Password Change Form
class passChangeForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label='Old Password',
                      widget=forms.PasswordInput(attrs={
                            'placeholder' : 'Old Password',
                            'class' : 'form-control'
                      }),
                      error_messages={
                        'required': 'Old Password Required.'})

    new_password1 = forms.CharField(required=True, label='New Password',
                    widget=forms.PasswordInput(attrs={
                            'placeholder' : 'New Password',
                            'class' : 'form-control'
                      }),
                    error_messages={'required': 'New Password Required.'},
                    min_length=8,
                    max_length=50)
    new_password2 = forms.CharField(required=True, label='Confirm Password',
                    widget=forms.PasswordInput(attrs={
                            'placeholder' : 'Confirm Password',
                            'class' : 'form-control'
                      }),
                    error_messages={'required': 'Confirm Password Required.'},
                    min_length=8,
                    max_length=50)


# Profile Edit Form
class profile_change_form(forms.Form):

    firstName = forms.CharField(label = "First Name",
            error_messages = {'required' : 'First Name Required.'},
            max_length = 100,
            widget = forms.TextInput(
                attrs = {
                    'placeholder' : 'First Name',
                    'class' : 'form-control'
                }
                )
            )
        
    lastName = forms.CharField(label = "Last Name",
        error_messages = {'required' : 'Last Name Required.'},
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'placeholder' : 'Last Name',
                'class' : 'form-control'
                }
            )
        )
        
    email = forms.CharField(label = "New Email", required=False,
        error_messages = {'required' : 'New Email Required.'},
        max_length = 100,
        widget = forms.EmailInput(
            attrs = {
                'placeholder' : 'Email',
                'class' : 'form-control'
                }
            )
        )
    
    profile_pic = forms.CharField(label= "Choose Your Profile Pic", required=False,
        widget = forms.FileInput(
            attrs = {
                'class' : 'form-control'
                }
            )
        )

    
    def clean_email(self):
        data = self.cleaned_data['email']

        if not User.objects.filter(email = data).exists():
            if not '@umail.ucc.ie' in data:
                raise ValidationError("Please add your official email")
            elif len(data.split('@')[1]) != 12:
                raise ValidationError("Please add your official email")
        return data