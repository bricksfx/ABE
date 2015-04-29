import time
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def handle_uploaded_file(f, user_name):
    print os.getcwd()
    file_name = unicode(f.name)
    print type(file_name)
    print file_name
    path = "./files/upload/" + user_name + time.strftime("/%Y/%m/%d/")
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path + file_name
    destination = open(file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)

    destination.close()

if __name__ == '__main__':
    print os.getcwd()