from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import *


# Create your views here.

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')
    return render(request, 'app/login.html')


@csrf_exempt
def dologin(request):
    if request.session.get('is_login', None):
        return JsonResponse({'status': '2'})
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        res = User.objects.filter(Q(username__exact=username) & Q(password__exact=password))
        if len(res) == 0:
            # 用户不存在
            return JsonResponse({'status': '0'})
        else:
            # 验证成功
            request.session['is_login'] = True
            request.session['user_id'] = res[0].id
            request.session['user_name'] = res[0].username
            # return redirect('/index/')
            return JsonResponse({'status': '1'})


def register(request):
    return render(request, 'app/register.html')


@csrf_exempt
def doregister(request):
    if request.method == "POST":
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


def index(request):
    if request.session.get('is_login', None) is None:
        return render(request, 'app/login.html')
    return render(request, 'app/index.html')


def adlisting(request):
    if request.session.get('is_login', None) is None:
        return render(request, 'app/login.html')
    return render(request, 'app/ad-listing.html')


def do_adlisting(request):
    pass


