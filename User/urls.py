from django.conf.urls import patterns, url
from User.views import login

urlpatterns = patterns('',
                       url('^login', login, name="login"),

                       )
