from django.conf.urls import url
from django.urls import path

from app import views

urlpatterns = [
    path(r'', views.login),
    url(r'^register/$', views.register),
    url(r'^doregister/$', views.doregister),
]
