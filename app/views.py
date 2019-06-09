from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
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
    dic, variable, book, book1, book2, book3, book4 = dict(), dict(), dict(), dict(), dict(), dict(), dict()
    book['book1'] = book1
    book['book2'] = book2
    book['book3'] = book3
    book['book4'] = book4
    # type category
    catList = ['aa', 'ab', 'ac', 'ad', 'ba', 'bb', 'bc', 'bd', 'ca', 'cb', 'cc', 'cd', 'da', 'db', 'dc', 'dd',
               'ea', 'eb', 'ec', 'ed', 'fa', 'fb', 'fc', 'fd', 'ga', 'gb', 'gc', 'gd', 'ha', 'hb', 'hc', 'hd']
    languageDic = {'EN': '英文', 'ZH': '中文', 'OT': '其他语言'}
    typeDic = {'1': '教育', '2': '文艺', '3': '人文社科', '4': '生活', '5': '经管', '6': '科技', '7': '少儿', '8': '励志'}
    for i in catList:
        variable[i] = BookCount.objects.get(cat=i).num
    dic['variable'] = variable
    # title type lan info
    books = Book.objects.all()[:4]
    for i, key in enumerate(book):
        book[key]['title'] = books[i].title
        book[key]['type'] = typeDic[books[i].type]
        book[key]['lan'] = languageDic[books[i].language]
        book[key]['info'] = books[i].info
        book[key]['url'] = books[i].img.url
    dic['book'] = book
    return render(request, 'app/index.html', dic)


def adlisting(request):
    if request.session.get('is_login', None) is None:
        return render(request, 'app/login.html')
    return render(request, 'app/ad-listing.html')


@csrf_exempt
def do_adlisting(request):
    if request.session.get('is_login', None) is None:
        # 未登录
        return JsonResponse({'flag': '0'})
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        language = request.POST.get('language')
        _type = request.POST.get('type')
        category = request.POST.get('category')
        info = request.POST.get('info')
        origin = request.POST.get('origin')
        sell = request.POST.get('sell')
        trade = request.POST.get('trade')
        isbn = request.POST.get('isbn')
        url = request.POST.get('url')
        img = request.FILES.get('img')

        cat_s = chr(ord(_type) - ord('1') + ord('a')) + chr(ord(category) - ord('1') + ord('a'))
        print(cat_s)
        num = BookCount.objects.get(cat=cat_s).num
        BookCount.objects.filter(cat=cat_s).update(num=num + 1)
        # print(title, author, language, _type, category, info, origin,
        #       sell, trade, isbn, url, img)
        book = Book()
        book.title = title
        book.author = author
        if language == 'chinese':
            book.language = 'ZH'
        elif language == 'english':
            book.language = 'EN'
        else:
            book.language = 'OT'
        book.type = _type
        book.category = category
        book.info = info
        book.originPrice = origin
        book.sellingPrice = sell
        book.isbn = isbn
        book.url = url
        book.img = img
        if trade == 'online':
            book.trade = 'OL'
        else:
            book.trade = 'FL'
        book.seller_id = request.session.get('user_id')
        book.save()
        print(str(book.img))
        _img = Image.open('media/' + str(book.img))
        print(_img.size)
        _img = _img.resize((275, 280), Image.ANTIALIAS)
        _img.save('media/' + str(book.img))
        return JsonResponse({'flag': '1'})
    return JsonResponse({'flag': '2'})
