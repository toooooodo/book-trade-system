from django.conf.urls import url
from django.urls import path, re_path

from app import views

urlpatterns = [
    path(r'', views.index, name='index'),
    url(r'^404$', views.notFound),
    url(r'^index/$', views.index),
    url(r'^login/$', views.login),
    url(r'^dologin/$', views.dologin),
    url(r'^register/$', views.register),
    url(r'^doregister/$', views.doregister),
    url(r'^adlisting/$', views.adlisting),
    url(r'^doadlisting/$', views.do_adlisting),
    re_path(r'^book/(?P<book_id>\d+)$', views.single_book, name='book'),
    re_path(r'^list/(?P<type_id>\d+)/(?P<page>\d+)$', views.show_list, name='list')
]
