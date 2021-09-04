from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from immi_fourm.models import forum_post
from immi_theme.models import notification


class immu_theme():
    
    def home(request):
        contex = {
            'notification': notification.objects.all().order_by('-date')
        }
        return render(request, 'theme/home.html', contex)
    
    # Users Accommodation Page
    @login_required
    def accommodation(request):
        contex = {
            'notification': notification.objects.all().order_by('-date')
        }
        return render(request, 'dashboard/accommodation.html', contex)


    # Users Immigration Page
    @login_required
    def immigration(request):
        contex = {
            'notification': notification.objects.all().order_by('-date')
        }
        return render(request, 'dashboard/immigration.html', contex)

    # Covid Info Page
    @login_required
    def covid_info(request):
        contex = {
            'notification': notification.objects.all().order_by('-date')
        }
        return render(request, 'dashboard/covid-info.html', contex)

    # Notifications
    @login_required
    def notifications(request):
        if request.method == 'GET' and request.is_ajax():
            all_notification = notification.objects.filter(user=request.user.username)
            for x in all_notification:
                x.view = True
                x.save()
            return JsonResponse({'results':'done'})
        else:
            pass