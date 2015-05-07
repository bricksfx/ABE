import time
import os
from django.core.files import File
from ABE.settings import MEDIA_ROOT


def make_file_path_for_model(user_name):

    path = MEDIA_ROOT + '/file/' + user_name + time.strftime("/%Y/%m/%d/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def handle_uploaded_file(f, user_name):

    file_name = unicode(f.name)
    path = MEDIA_ROOT + '/tmp/' + user_name + time.strftime("/%Y/%m/%d/")
    print 'path in function', path
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path + file_name
    destination = open(file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    path = file_name
    return path


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
        return True
    else:
        return False

if __name__ == '__main__':
    print os.getcwd()