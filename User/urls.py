from django.conf.urls import patterns, url
from User.views import *

urlpatterns = patterns('',
                       url('^login', login, name="login"),
                       url('^index', index, name="index"),
                       )
