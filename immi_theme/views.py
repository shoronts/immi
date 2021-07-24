from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from immi_fourm.models import forum_post

from .forms import search_form


class immu_theme():
    
    def home(request):
        return render(request, 'theme/home.html')

    @login_required
    def search(request):
        if request.method == 'POST':
            search = search_form(request.POST)
            if search.is_valid():
                search_content = search.cleaned_data['search']
                try:
                    search_datas = forum_post.objects.filter(title__contains=search_content)
                except:
                    search_datas = None
                contex = {
                    'search_content':search_content,
                    'search_datas' : search_datas,
                    'search' : search_form()
                }
                return render(request, 'theme/search.html', contex)
            
        else:
            search = search_form()
        return render(request, 'theme/search.html', {'search':search})
