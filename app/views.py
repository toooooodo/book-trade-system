from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import *


# Create your views here.

def login(request):
    return render(request, 'app/login.html')


def register(request):
    return render(request, 'app/register.html')


@csrf_exempt
def doregister(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    print(username, email, password)
    # res = User.objects.filter(username=username, email=email)
    # res = User.objects.filter(Q(username__exact=username) | Q(email__exact=email))
    res_user = User.objects.filter(username=username)
    res_email = User.objects.filter(email=email)
    if len(res_user) == 0 and len(res_email) == 0:
        u = User()
        u.username = username
        u.password = password
        u.email = email
        u.save()
        return_dict = {'status': '0'}
        return JsonResponse(return_dict)
    elif len(res_user) == 0:
        # 邮箱已被注册
        return_dict = {'status': '1'}
        return JsonResponse(return_dict)
    else:
        # 用户名已被注册
        return_dict = {'status': '2'}
        return JsonResponse(return_dict)
