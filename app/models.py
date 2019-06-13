from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class User(models.Model):
#     username = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=25)
#     email = models.EmailField(max_length=25, unique=True)
#     time = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    BOOK_TYPE_CHOICES = (
        ('1', 'education'),  # 教育
        ('2', 'literary'),  # 文艺
        ('3', 'humanities'),  # 人文社科
        ('4', 'life'),  # 生活
        ('5', 'economic'),  # 经管
        ('6', 'tech'),  # 科技
        ('7', 'child'),  # 少儿
        ('8', 'Inspirational'),  # 励志
    )
    BOOK_LAN_CHOICES = (
        ('EN', 'english'),  # 英语
        ('ZH', 'chinese'),  # 汉语
        ('OT', 'other'),  # 其他
    )
    TRADE_TYPE = (
        ('OL', 'online'),  # 线上
        ('FL', 'offline'),  # 线下
    )
    seller = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)  # 卖方
    title = models.CharField(max_length=80)  # 书名
    author = models.CharField(max_length=40)  # 作者
    language = models.CharField(max_length=2, choices=BOOK_LAN_CHOICES)  # 语言
    originPrice = models.DecimalField(max_digits=6, decimal_places=2)  # 原价
    sellingPrice = models.DecimalField(max_digits=6, decimal_places=2)  # 售价
    type = models.CharField(max_length=1, choices=BOOK_TYPE_CHOICES)  # 种类
    category = models.CharField(max_length=1)
    info = models.TextField()  # 描述
    img = models.ImageField(upload_to='images')  # 图片
    isbn = models.CharField(max_length=20)
    url = models.URLField()
    trade = models.CharField(max_length=2, choices=TRADE_TYPE)  # 交易方式
    time = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField()
    score = models.DecimalField(max_digits=2, decimal_places=1)

    def getSeller(self):
        return self.seller


# class EDBook(models.Model):
#     id = models.IntegerField(primary_key=True)
#     category = models.CharField(max_length=1)
#
#
# class LTBook(models.Model):
#     id = models.IntegerField(primary_key=True)
#     category = models.CharField(max_length=1)
#
#
# class HMBook(models.Model):
#     id = models.IntegerField(primary_key=True)
#     category = models.CharField(max_length=1)
#
#
# class LFBook(models.Model):
#     id = models.IntegerField(primary_key=True)
#     category = models.CharField(max_length=1)
#
#
# class ECBook(models.Model):
#     id = models.IntegerField(primary_key=True)
#     category = models.CharField(max_length=1)
#
#
# class TCBook(models.Model):
#     id = models.IntegerField(primary_key=True)
#     category = models.CharField(max_length=1)
#
#
# class CHBook(models.Model):
#     id = models.IntegerField(primary_key=True)
#     category = models.CharField(max_length=1)
#
#
# class INBook(models.Model):
#     id = models.IntegerField(primary_key=True)
#     category = models.CharField(max_length=1)
#
#
class BookCount(models.Model):
    cat = models.CharField(max_length=2, primary_key=True)
    num = models.IntegerField()


class OrderForm(models.Model):
    TRADE_TYPE = (
        ('OL', 'online'),  # 线上
        ('FL', 'offline'),  # 线下
    )
    seller = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    buyer = models.IntegerField()
    method = models.CharField(max_length=2, choices=TRADE_TYPE)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    timeorname = models.CharField(max_length=30)
    message = models.TextField()
    book = models.ForeignKey('Book', to_field='id', on_delete=models.CASCADE)

    def getSeller(self):
        return self.seller


class Want(models.Model):
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    author = models.CharField(max_length=40)
    disc = models.TextField()
    # isbn = models.CharField(max_length=20, null=True, blank=True)
    img = models.ImageField(upload_to='images')  # 图片
    time = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField()

    def getWanter(self):
        return self.user
