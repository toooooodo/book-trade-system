from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=25)
    email = models.EmailField(max_length=25, unique=True)


class Book(models.Model):
    BOOK_TYPE_CHOICES = (
        ('LT', 'literature'),  # 文学
        ('CH', 'child'),  # 少儿
        ('ED', 'education'),  # 教育
        ('HM', 'humanities'),  # 人文
        ('LF', 'life'),  # 生活
        ('AT', 'art'),  # 艺术
        ('TC', 'tech'),  # 科技
        ('CS', 'computer'),  # 计算机
    )
    BOOK_LAN_CHOICES = (
        ('EN', 'english'),  # 英语
        ('ZH', 'chinese'),  # 汉语
        ('OT', 'other'),  # 其他
    )
    seller = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=15)
    language = models.CharField(max_length=2, choices=BOOK_LAN_CHOICES)
    originPrice = models.DecimalField(max_digits=6, decimal_places=2)
    sellingPrice = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(max_length=2, choices=BOOK_TYPE_CHOICES)
    info = models.CharField(max_length=255)
    img = models.ImageField()
    isbn = models.CharField(max_length=20, blank=True)
    url = models.URLField()
    time = models.DateTimeField(auto_now_add=True)


class OrderForm(models.Model):
    TRADE_TYPE = (
        ('OL', 'online'),  # 线上
        ('FL', 'offline'),  # 线下
    )
    seller = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE)
    buyer = models.IntegerField()
    method = models.CharField(max_length=2, choices=TRADE_TYPE)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    book = models.ForeignKey('Book', to_field='id', on_delete=models.CASCADE)


class Want(models.Model):
    user = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=15, null=True, blank=True)
    disc = models.TextField()
    isbn = models.CharField(max_length=20, null=True, blank=True)
    url = models.URLField()
