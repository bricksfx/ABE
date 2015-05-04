import time
import os
from django.core.files import File
from ABE.settings import MEDIA_ROOT

def handle_uploaded_file(f, user_name):
    print os.getcwd()
    file_name = unicode(f.name)
    print type(file_name)
    print file_name
    path = MEDIA_ROOT + user_name + time.strftime("/%Y/%m/%d/")
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path + file_name
    destination = open(file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)

    return File(destination)

if __name__ == '__main__':
    print os.getcwd()