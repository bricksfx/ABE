from django.conf.urls import patterns, url
from User.views import *

urlpatterns = patterns('',
                       url('^login', Login, name="login"),
                       url('^register/$', Register, name="register"),
                       url('^logout/$', Logout, name="logout"),
                       url('^index', index, name="index"),
                       url('^upload/$', upload_file, name="upload"),
                       url('^download/$', download_file, name="download"),
                       url('^share/$', share_file, name='share'),
                       url('^list/$', list_file, name='list'),
                       )
