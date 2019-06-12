from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import datetime
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
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


def login(request):
    """
    登陆页面
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        return redirect('/index')
    return render(request, 'app/login.html')


@csrf_exempt
def dologin(request):
    """
    登录处理
    :param request:
    :return:
    """
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
    """
    首页
    :param request:
    :return:
    """
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
    typeDic = {'1': '教育', '2': '文艺', '3': '人文社科', '4': '生活', '5': '经管', '6': '科技', '7': '少儿', '8': '励志'}
    for i in catList:
        variable[i] = BookCount.objects.get(cat=i).num
    dic['variable'] = variable
    # title type lan info
    books = Book.objects.filter(sold__exact=False)[:4]
    for i, key in enumerate(book):
        book[key]['title'] = books[i].title
        book[key]['type'] = typeDic[books[i].type]
        # book[key]['lan'] = languageDic[books[i].language]
        book[key]['time'] = books[i].time
        book[key]['info'] = books[i].info
        book[key]['url'] = books[i].img.url
        book[key]['id'] = books[i].id
    dic['book'] = book
    return render(request, 'app/index.html', dic)


def adlisting(request):
    """
    发布商品
    :param request:
    :return:
    """

    if request.session.get('is_login', None) is None:
        return render(request, 'app/login.html')
    return render(request, 'app/ad-listing.html')


@csrf_exempt
def do_adlisting(request):
    """
    处理发布商品请求
    :param request:
    :return:
    """
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
        book.sold = False
        book.score = 5.0
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
    seller_re = User.objects.filter(id=book_re[0].seller_id)[0]
    book_re = book_re[0]
    tradeDic = {'OL': '线上', 'FL': '线下'}
    lanDic = {'EN': '英文', 'ZH': '中文', 'OT': '其他'}
    typeDic = {'1': '教育', '2': '文艺', '3': '人文社科', '4': '生活', '5': '经管', '6': '科技', '7': '少儿', '8': '励志'}
    dic = dict()
    book = model_to_dict(book_re,
                         fields=['id', 'title', 'author', 'info', 'isbn', 'url'])
    seller = model_to_dict(seller_re, fields=['username'])
    seller['time'] = seller_re.time
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
    # dic['buyer'] = request.session.get('user_id')
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
        if '0' <= type_id <= '8':
            sort = request.GET.get('sort')
            title = request.GET.get('title')
            if type_id == '0':
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

        contest = {
            'pages': pages,
            'sort': sort,
            'book_page': book_page,
            'type': type_id,
            'title': title,
            'total': len(books),
            'time': datetime.datetime.now(),
            'count': count,
        }
        return render(request, 'app/ad-list-view.html', contest)
    return render(request, 'app/404.html')


def order(request, book_id):
    """
    订单页
    :param request:
    :param book_id:
    :return:
    """
    if request.session.get('is_login', None) is None:
        return render(request, 'app/login.html')
    # buyer = request.session.get('user_id')
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
        'seller': User.objects.filter(id=book[0].seller_id)[0].username
    }
    print(bookDic)
    return render(request, 'app/order.html', context)


def doOrder(request):
    """
    处理订单请求
    :param request:
    :return:
    """
    if request.session.get('is_login', None) is None:
        return JsonResponse({'flag': '2'})
    if request.method == "GET":
        return JsonResponse({'flag': '2'})
    orderform = OrderForm()
    print(request.session.get('user_id'))
    orderform.buyer = request.session.get('user_id')
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


def want(request):
    if request.session.get('is_login', None) is None:
        return render(request, 'app/login.html')
    return render(request, 'app/want.html')


@csrf_exempt
def dowant(request):
    if request.session.get('is_login', None) is None:
        # 未登录
        return JsonResponse({'flag': '0'})
    if request.method == "POST":
        _want = Want()
        _want.title = request.POST.get('title')
        _want.author = request.POST.get('author')
        _want.disc = request.POST.get('info')
        _want.user_id = request.session.get('user_id')
        _want.img = request.FILES.get('img')
        _want.save()
        _img = Image.open('media/' + str(_want.img))
        print(_img.size)
        _img = _img.resize((275, 280), Image.ANTIALIAS)
        _img.save('media/' + str(_want.img))
        return JsonResponse({'flag': '1'})
    return JsonResponse({'flag': '2'})
