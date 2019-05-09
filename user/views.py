from django.shortcuts import render
from django.http import HttpResponseRedirect


# Create your views here.


def user_mail(request):
    if request.user.is_authenticated:
        context = {
            'name': request.user.first_name,
            'mail': request.user.email,
        }
        return render(request, 'user/user.html', context)
    else:
        return HttpResponseRedirect('/account/login')

