from django.conf.urls import url
from django.urls import path

from app import views

urlpatterns = [
    path(r'', views.index),
    url(r'^index/$', views.index),
    url(r'^login/$', views.login),
    url(r'^dologin/$', views.dologin),
    url(r'^register/$', views.register),
    url(r'^doregister/$', views.doregister),
]
