from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=25)
    email = models.EmailField(max_length=25, unique=True)


class Book(models.Model):
    BOOK_TYPE_CHOICES = (
        ('LT', 'literature'),
        ('CH', 'child'),
        ('ED', 'education'),
        ('HM', 'humanities'),
        ('LF', 'life'),
        ('AT', 'art'),
        ('TC', 'tech'),
        ('CS', 'computer'),
    )
    BOOK_LAN_CHOICES = (
        ('EN', 'english'),
        ('ZH', 'chinese'),
        ('OT', 'other'),
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
        ('OL', 'online'),
        ('FL', 'offline'),
    )
    seller = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE)
    buyer = models.IntegerField()
    method = models.CharField(max_length=2, choices=TRADE_TYPE)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    book = models.ForeignKey('Book', to_field='id', on_delete=models.CASCADE)


class Want(models.Model):
    user = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=15, null=True, blank=True)
    disc = models.TextField()
    isbn = models.CharField(max_length=20, null=True, blank=True)
    url = models.URLField()
