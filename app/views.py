from django.contrib.auth import authenticate, login, logout, hashers
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import datetime
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from notifications.signals import notify
from PIL import Image
from app.models import *


# Create your views here.


def notFound(request):
    """
    404
    :param request:
    :return:
    """
    return render(request, 'app/404.html')


def login_view(request):
    """
    登陆页面
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('/index')
    return render(request, 'app/login.html')


@csrf_exempt
def dologin(request):
    """
    登录处理
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return JsonResponse({'status': '2'})
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # res = User.objects.filter(Q(username__exact=username) & Q(password__exact=password))
        user = authenticate(request, username=username, password=password)
        if user is None:
            # 用户不存在
            return JsonResponse({'status': '0'})
        else:
            # 验证成功
            login(request, user)
            return JsonResponse({'status': '1'})


def register(request):
    """
    注册页面
    :param request:
    :return:
    """
    return render(request, 'app/register.html')


@csrf_exempt
def doregister(request):
    """
    注册处理
    :param request:
    :return:
    """
    if request.method == "POST":
        username = (request.POST.get('username')).strip()
        email = (request.POST.get('email')).strip()
        password = (request.POST.get('password')).strip()
        print(username, email, password)
        # res = User.objects.filter(username=username, email=email)
        # res = User.objects.filter(Q(username__exact=username) | Q(email__exact=email))
        res_user = MyUser.objects.filter(username=username)
        res_email = MyUser.objects.filter(email=email)
        if len(res_user) == 0 and len(res_email) == 0:
            u = MyUser.objects.create_user(username=username, email=email, password=password)
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
    """
    首页
    :param request:
    :return:
    """
    print(request.user.id)  # username
    dic, variable, book, book1, book2, book3, book4 = dict(), dict(), dict(), dict(), dict(), dict(), dict()
    book['book1'] = book1
    book['book2'] = book2
    book['book3'] = book3
    book['book4'] = book4
    # type category
    catList = ['aa', 'ab', 'ac', 'ad', 'ba', 'bb', 'bc', 'bd', 'ca', 'cb', 'cc', 'cd', 'da', 'db', 'dc', 'dd',
               'ea', 'eb', 'ec', 'ed', 'fa', 'fb', 'fc', 'fd', 'ga', 'gb', 'gc', 'gd', 'ha', 'hb', 'hc', 'hd']
    typeDic = {'1': '教育', '2': '文艺', '3': '人文社科', '4': '生活', '5': '经管', '6': '科技', '7': '少儿', '8': '励志'}
    for i in catList:
        variable[i] = BookCount.objects.get(cat=i).num
    dic['variable'] = variable
    # title type lan info
    books = Book.objects.filter(sold__exact=False)[:4]
    if len(books) == 4:
        for i, key in enumerate(book):
            book[key]['title'] = books[i].title
            book[key]['type'] = typeDic[books[i].type]
            # book[key]['lan'] = languageDic[books[i].language]
            book[key]['time'] = books[i].time
            book[key]['info'] = books[i].info
            book[key]['url'] = books[i].img.url
            book[key]['id'] = books[i].id
        dic['flag'] = True
    else:
        dic['flag'] = False
    dic['book'] = book
    return render(request, 'app/index.html', dic)


@login_required
def adlisting(request):
    """
    发布商品
    :param request:
    :return:
    """
    return render(request, 'app/ad-listing.html')


@csrf_exempt
def do_adlisting(request):
    """
    处理发布商品请求
    :param request:
    :return:
    """
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
        book.sold = False
        book.score = 5.0
        if trade == 'online':
            book.trade = 'OL'
        else:
            book.trade = 'FL'
        book.seller_id = request.user.id
        book.save()
        print(str(book.img))
        _img = Image.open('media/' + str(book.img))
        print(_img.size)
        _img = _img.resize((800, 800), Image.ANTIALIAS)
        _img.save('media/' + str(book.img))
        return JsonResponse({'flag': '1'})
    return JsonResponse({'flag': '2'})


def single_book(request, book_id):
    """
    商品详情页
    :param request:
    :param book_id:
    :return:
    """
    book_re = Book.objects.filter(id=book_id, sold=False)
    if len(book_re) == 0:
        return render(request, 'app/404.html')
    for i in book_re:
        print(i)
    seller_re = MyUser.objects.filter(id=book_re[0].seller_id)[0]
    book_re = book_re[0]
    tradeDic = {'OL': '线上', 'FL': '线下'}
    lanDic = {'EN': '英文', 'ZH': '中文', 'OT': '其他'}
    typeDic = {'1': '教育', '2': '文艺', '3': '人文社科', '4': '生活', '5': '经管', '6': '科技', '7': '少儿', '8': '励志'}
    dic = dict()
    book = model_to_dict(book_re,
                         fields=['id', 'title', 'author', 'info', 'isbn', 'url'])
    seller = model_to_dict(seller_re, fields=['username', 'id'])
    seller['time'] = seller_re.date_joined
    book['trade'] = tradeDic[book_re.trade]
    book['lan'] = lanDic[book_re.language]
    book['type'] = typeDic[book_re.type]
    book['origin'] = float(book_re.originPrice)
    book['selling'] = float(book_re.sellingPrice)
    book['score'] = float(book_re.score)
    book['img'] = book_re.img.url
    book['time'] = book_re.time
    dic['book'] = book
    dic['seller'] = seller
    print(dic)
    return render(request, 'app/single.html', dic)


def show_list(request, type_id, page):
    """
    商品列表
    :param request:
    :param type_id:
    :param page:
    :return:
    """
    if request.method == "GET":
        if '0' <= str(type_id) <= '8':
            sort = request.GET.get('sort')
            title = request.GET.get('title')
            if str(type_id) == '0':
                if sort == 'ascending':
                    books = Book.objects.filter(title__contains=title, sold__exact=False).order_by('sellingPrice')
                elif sort == 'descending':
                    books = Book.objects.filter(title__contains=title, sold__exact=False).order_by('-sellingPrice')
                elif sort == 'latest':
                    books = Book.objects.filter(title__contains=title, sold__exact=False).order_by('-id')
                else:
                    return render(request, 'app/404.html')
            else:
                if sort == 'ascending':
                    books = Book.objects.filter(title__contains=title, type__exact=type_id, sold__exact=False).order_by(
                        'sellingPrice')
                elif sort == 'descending':
                    books = Book.objects.filter(title__contains=title, type__exact=type_id, sold__exact=False).order_by(
                        '-sellingPrice')
                elif sort == 'latest':
                    books = Book.objects.filter(title__contains=title, type__exact=type_id, sold__exact=False).order_by(
                        '-id')
                else:
                    return render(request, 'app/404.html')
        else:
            return render(request, 'app/404.html')

        paginator = Paginator(books, 4)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            return render(request, 'app/404.html')

        if page > paginator.num_pages or page <= 0:
            return render(request, 'app/404.html')

        # 获取第page页的Page实例对象
        book_page = paginator.page(page)
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        print(book_page)

        count = {'1': '教育', '2': '文艺', '3': '人文社科', '4': '生活', '5': '经管', '6': '科技', '7': '少儿', '8': '励志'}
        # typeDic = {'1': '教育', '2': '文艺', '3': '人文社科', '4': '生活', '5': '经管', '6': '科技', '7': '少儿', '8': '励志'}
        for key in count:
            count[key] = len(Book.objects.filter(title__contains=title, type__exact=key, sold__exact=False))

        context = {
            'pages': pages,
            'sort': sort,
            'book_page': book_page,
            'type': type_id,
            'title': title,
            'total': len(books),
            'time': datetime.datetime.now(),
            'count': count,
        }
        return render(request, 'app/ad-list-view.html', context)
    return render(request, 'app/404.html')


@login_required
def order(request, book_id):
    """
    订单页
    :param request:
    :param book_id:
    :return:
    """
    book = Book.objects.filter(id=book_id, sold__exact=False)
    if len(book) == 0:
        return render(request, 'app/order.html')
    # print(book[0].title)
    typeDic = {'1': '教育', '2': '文艺', '3': '人文社科', '4': '生活', '5': '经管', '6': '科技', '7': '少儿', '8': '励志'}
    bookDic = model_to_dict(book[0], fields=['id', 'title', 'trade', 'sellingPrice'])
    bookDic['type'] = typeDic[book[0].type]
    bookDic['img'] = book[0].img.url
    bookDic['time'] = book[0].time
    context = {
        'book': bookDic,
        'seller': MyUser.objects.filter(id=book[0].seller_id)[0].username
    }
    print(bookDic)
    return render(request, 'app/order.html', context)


@login_required
def doOrder(request):
    """
    处理订单请求
    :param request:
    :return:
    """
    if request.method == "GET":
        return JsonResponse({'flag': '2'})
    orderform = OrderForm()
    orderform.buyer = request.user.id
    orderform.phone = request.POST.get('phone')
    orderform.address = request.POST.get('address')
    orderform.timeorname = request.POST.get('timeorname')
    orderform.message = request.POST.get('message')
    orderform.book_id = request.POST.get('book_id')
    # print(orderform.buyer, orderform.phone, orderform.address, orderform.timeorname, orderform.message,
    #       orderform.book_id)
    book = Book.objects.filter(id=orderform.book_id, sold__exact=False)

    # print(book[0].seller)   seller是个对象
    if len(book) == 0:
        # 没有此书
        return JsonResponse({'flag': '0'})
    elif book[0].seller_id == orderform.buyer:
        # 卖方和买方是同一人
        return JsonResponse({'flag': '3'})
    else:
        orderform.seller_id = book[0].seller_id
        orderform.method = book[0].trade
        book[0].sold = True
        # update book
        book[0].save()
        # save order
        orderform.save()
        # update book count
        cat_s = chr(ord(book[0].type) - ord('1') + ord('a')) + chr(ord(book[0].category) - ord('1') + ord('a'))
        print(cat_s)
        num = BookCount.objects.get(cat=cat_s).num
        BookCount.objects.filter(cat=cat_s).update(num=num - 1)
        return JsonResponse({'flag': '1'})


@login_required
def want(request):
    return render(request, 'app/want.html')


@csrf_exempt
def dowant(request):
    if not request.user.is_authenticated:
        # 未登录
        return JsonResponse({'flag': '0'})
    if request.method == "POST":
        _want = Want()
        _want.title = request.POST.get('title')
        _want.author = request.POST.get('author')
        _want.disc = request.POST.get('info')
        _want.user_id = request.user.id
        _want.img = request.FILES.get('img')
        _want.flag = True
        _want.save()
        _img = Image.open('media/' + str(_want.img))
        print(_img.size)
        _img = _img.resize((800, 800), Image.ANTIALIAS)
        _img.save('media/' + str(_want.img))
        return JsonResponse({'flag': '1'})
    return JsonResponse({'flag': '2'})


def showWantList(request, page):
    if request.method == "GET":
        sort = request.GET.get('sort')
        if sort == 'latest':
            wantList = Want.objects.filter(flag__exact=True).order_by('-id')
        elif sort == 'earliest':
            wantList = Want.objects.filter(flag__exact=True).order_by('id')
        else:
            return render(request, 'app/404.html')
        paginator = Paginator(wantList, 9)
        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            return render(request, 'app/404.html')

        if page > paginator.num_pages or page <= 0:
            return render(request, 'app/404.html')

        # 获取第page页的Page实例对象
        want_page = paginator.page(page)
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)
        context = {
            'pages': pages,
            'sort': sort,
            'want_page': want_page,
            'total': len(wantList),
            'time': datetime.datetime.now(),
        }
        return render(request, 'app/want-list.html', context)
    else:
        return render(request, 'app/404.html')


def test(request):
    return render(request, 'app/test.html')


@csrf_exempt
@login_required
def noti(request, seller_id, book_id):
    if request.method == "POST":
        notify.send(request.user, recipient=MyUser.objects.filter(id=seller_id), verb=request.POST.get('message'),
                    target=Book.objects.filter(id=book_id)[0])
        return redirect(reverse('book', args=[book_id]))
    return render(request, 'app/404.html')


@login_required
def message(request, page):
    user = MyUser.objects.get(id=request.user.id)
    messages = user.notifications.active()
    paginator = Paginator(messages, 5)
    # 获取第page页的内容
    try:
        page = int(page)
    except Exception as e:
        return render(request, 'app/404.html')
    if page > paginator.num_pages or page <= 0:
        return redirect(reverse('message', args=[1]))
    message_page = paginator.page(page)
    num_pages = paginator.num_pages
    if num_pages < 5:
        pages = range(1, num_pages + 1)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page - 2, page + 3)
    context = {
        'pages': pages,
        'message_page': message_page,
    }
    return render(request, 'app/message.html', context)


@login_required
def readMessage(request, page_id, message_id):
    request.user.notifications.get(id=message_id).mark_as_read()
    return redirect(reverse('message', args=[page_id]))


@login_required
def deleteMessage(request, page_id, message_id):
    # request.user.notifications.get(id=message_id).deleted()
    notifi = request.user.notifications.get(id=message_id)
    notifi.deleted = True
    notifi.save()
    return redirect(reverse('message', args=[page_id]))


@login_required
def myAd(request, page):
    books = Book.objects.filter(seller_id=request.user.id, sold__exact=False).order_by('id')
    paginator = Paginator(books, 4)
    # 获取第page页的内容
    try:
        page = int(page)
    except Exception as e:
        return render(request, 'app/404.html')

    if page > paginator.num_pages or page <= 0:
        return redirect(reverse('my-ad', args=[1]))
    book_page = paginator.page(page)
    num_pages = paginator.num_pages
    if num_pages < 5:
        pages = range(1, num_pages + 1)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page - 2, page + 3)
    typeDic = {'1': '教育', '2': '文艺', '3': '人文社科', '4': '生活', '5': '经管', '6': '科技', '7': '少儿', '8': '励志'}

    for i in book_page:
        i.type = typeDic[i.type]
    context = {
        'pages': pages,
        'book_page': book_page,
    }
    return render(request, 'app/dashboard-my-ads.html', context)


@login_required
def edit(request):
    return render(request, 'app/user-profile.html')


@csrf_exempt
# @login_required
def editPerInfo(request):
    if not request.user.is_authenticated:
        # 未登录
        return JsonResponse({'flag': '0'})
    # print('edit personal info')
    if request.method == "POST":
        user = MyUser.objects.get(id=request.user.id)
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.portrait = request.FILES.get('portrait')
        user.save()
        _img = Image.open('media/' + str(user.portrait))
        _img = _img.resize((800, 800), Image.ANTIALIAS)
        _img.save('media/' + str(user.portrait))
        return JsonResponse({'flag': '1'})
    return JsonResponse({'flag': '2'})


@csrf_exempt
@login_required
def editPassword(request):
    print('111')
    if request.method == "POST":
        user = MyUser.objects.get(id=request.user.id)
        current = (request.POST.get('current')).strip()
        new = (request.POST.get('new')).strip()
        # print(user, current, new)
        if user.check_password(current):
            print('yes')
            if not new:
                # 新密码为空
                return JsonResponse({'flag': '2'})
            elif len(new) <= 6:
                return JsonResponse({'flag': '3'})
            else:
                user.password = hashers.make_password(password=new)
                user.save()
                logout(request)
                return JsonResponse({'flag': '1'})
        else:
            print('no')
            return JsonResponse({'flag': '0'})
    return JsonResponse({'flag': 'error'})


@csrf_exempt
@login_required
def editEmail(request):
    if request.method == "POST":
        user = MyUser.objects.get(id=request.user.id)
        current = (request.POST.get('current')).strip()
        new = (request.POST.get('new')).strip()
        if user.email == current:
            if len(MyUser.objects.filter(email__exact=new)) == 0:
                user.email = new
                user.save()
                return JsonResponse({'flag': '1'})
            else:
                return JsonResponse({'flag': '2'})
        else:
            return JsonResponse({'flag': '0'})
    return JsonResponse({'flag': 'error'})

@login_required
def logOut(request):
    logout(request)
    return redirect(reverse('index'))
