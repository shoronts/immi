from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from immi_theme.models import Notification


class ImmiTheme:
    
    def home(self):
        contex = {
            'notification': Notification.objects.all().order_by('-date')
        }
        return render(self, 'theme/home.html', contex)
    
    # Users Accommodation Page
    @login_required
    def accommodation(self):
        contex = {
            'notification': Notification.objects.all().order_by('-date')
        }
        return render(self, 'dashboard/accommodation.html', contex)

    # Users Immigration Page
    @login_required
    def immigration(self):
        contex = {
            'notification': Notification.objects.all().order_by('-date')
        }
        return render(self, 'dashboard/immigration.html', contex)

    # Covid Info Page
    @login_required
    def covid_info(self):
        contex = {
            'notification': Notification.objects.all().order_by('-date')
        }
        return render(self, 'dashboard/covid-info.html', contex)

    # Notifications
    @login_required
    def notifications(self):
        if self.method == 'GET' and self.is_ajax():
            all_notification = Notification.objects.filter(user=self.user.username)
            for x in all_notification:
                x.view = True
                x.save()
            return JsonResponse({'results': 'done'})
