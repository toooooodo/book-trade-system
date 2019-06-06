from django.shortcuts import render
from django.http import HttpResponse
from app.models import *


# Create your views here.

def login(request):
    return render(request, 'app/login.html')


def register(request):
    return render(request, 'app/register.html')


def doregister(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    res = User.objects.filter(username=username, email=email)
    print(res)
    if len(res) == 0:
        u = User()
        u.username = username
        u.password = password
        u.email = email
        u.save()
    else:
        print('No')
    return HttpResponse('daf')
