from django.conf.urls import url
from django.urls import path, re_path

from app import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path('404/', views.notFound, name='404'),
    path('index/', views.index),
    path('login/', views.login_view, name='login'),
    path('dologin/', views.dologin),
    path('register/', views.register, name='register'),
    path('doregister/', views.doregister),
    path('adlisting/', views.adlisting, name='adlisting'),
    path('doadlisting/', views.do_adlisting),
    path('book/<int:book_id>', views.single_book, name='book'),
    path('list/<int:type_id>/<int:page>', views.show_list, name='list'),
    path('order/<int:book_id>', views.order, name='order'),
    path('doorder/', views.doOrder, name='doorder'),
    path('want/', views.want, name='want'),
    path('dowant/', views.dowant, name='dowant'),
    path('want-list/<int:page>', views.showWantList, name='want-list'),
    path('test/', views.test, name='test'),
    path('noti/<int:seller_id>/<int:book_id>', views.noti, name='noti'),
    path('m-noti/<int:recipient>/<int:book_id>/<int:message_page>', views.messageNoti, name='m-noti'),
    path('message/<int:page>', views.message, name='message'),
    path('read-message/<int:page_id>/<int:message_id>', views.readMessage, name='read-message'),
    path('delete-message/<int:page_id>/<int:message_id>', views.deleteMessage, name='delete-message'),
    path('my-ad/<int:page>', views.myAd, name='my-ad'),
    path('edit/', views.edit, name='edit'),
    path('logout/', views.logOut, name='logout'),
    path('edit-personal-info/', views.editPerInfo, name='edit-personal-info'),
    path('edit-password/', views.editPassword, name='edit-password'),
    path('edit-email/', views.editEmail, name='edit-email'),
    path('cart/<int:page>', views.cart, name='cart'),
    path('add-cart/<int:book_id>', views.addItem, name='add-cart'),
    path('remove-cart/<int:book_id>', views.removeItem, name='remove-cart'),
]
