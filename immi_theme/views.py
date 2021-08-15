from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from immi_fourm.models import forum_post


class immu_theme():
    
    def home(request):
        return render(request, 'theme/home.html')
