from django.conf.urls import patterns, url
from User.views import *

urlpatterns = patterns('',
                       url('^login', login, name="login"),
                       url('^index', index, name="index"),
                       url('^upload/$', upload_file, name="upload"),
                       url('^download/$', download_file, name="download"),
                       url('^share/$', share_file, name='share'),
                       url('^list/$', list_file, name='list'),
                       )
