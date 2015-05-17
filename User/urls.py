from django.conf.urls import patterns, url
from User.views import *

urlpatterns = patterns('',
                       url('^login', Login, name="login"),
                       url('^register/$', Register, name="register"),
                       url('^logout/$', Logout, name="logout"),
                       url('^index', index, name="index"),
                       url('^upload/$', upload_file, name="upload"),
                       url('^download/$', download_file, name="download"),
                       url('^download_file/?file=(?P<file_id>\d+)/$', file_down_single, name="file_down_single"),
                       url('^delete_file/?file=(?P<file_id>\d+)/$', file_delete, name="file_delete"),
                       url('^share/$', share_file, name='share'),
                       url('^list/$', list_file, name='list'),
                       url('^file?.*/$', upload, name="test"),
                       url('^test_upload/$', test_upload, name="test_upload"),
                       url('^get_department/$', get_department, name="get_department"),
                       url('^improve_user_info/$', improve_user_info, name='improve_user_info'),
                       url('^get_department_multiple/$', get_department_multiple, name="get_department_multiple"),
                       )
