import time
import os
from django.core.files import File
from ABE.settings import MEDIA_ROOT

def handle_uploaded_file(f, user_name):
    print 'media_root', MEDIA_ROOT
    print type(f)
    file_name = unicode(f.name)
    print file_name
    path = MEDIA_ROOT + '/tmp/' + user_name + time.strftime("/%Y/%m/%d/")
    print 'path in function', path
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path + file_name
    destination = open(file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)

    return File(destination)

if __name__ == '__main__':
    print os.getcwd()