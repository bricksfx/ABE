import time
import os
from django.core.files import File
from ABE.settings import MEDIA_ROOT
from cripto import Crypto
from file_key_process import share_to_attr
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import pickle


def file_key_encrypt(user_id, file_id, share, key):
    print share
    path = BASE_DIR + '/key_info/' + str(user_id) + '/' + 'cripto_info.txt'
    cry = Crypto(400, "username")
    key_info = open(path, 'rb')
    key_file = pickle.load(key_info)
    cry.publicKey = key_file['publicKey']
    cry.masterkey = key_file['masterKey']
    cry.attributi = key_file['attributi']
    cry.keygenerator = key_file['keygenerator']
    key_info.close()
    print cry
    attr = share_to_attr(share)
    key_list = []
    for mess in key:
        E = cry.encrypto(ord(mess), attr)
        key_list.append(E)
    path_out = BASE_DIR + '/file_key/'
    if not os.path.exists(path_out):
        os.makedirs(path_out)
    path_out += str(file_id)
    file_out = open(path_out, 'wb')
    pickle.dump(key_list, file_out)
    file_out.close()

def set_user_abe_key_path(user_id):
    path = BASE_DIR + '/key_info/' + user_id + '/'
    print path
    if not os.path.exists(path):
        os.makedirs(path)
    path_of_key = path + 'cripto_info.txt'
    f = open(path_of_key, 'wb')
    cry = Crypto(400, "username")
    key_info = {'publicKey': cry.publicKey, 'masterKey': cry.masterKey,
                'attributi': cry.attributi, 'keygenerator': cry.keygenerator}
    pickle.dump(key_info, f)
    f.close()

def set_tmp_path(user_name):
    path = MEDIA_ROOT + '/tmp/' + user_name + time.strftime("/%Y/%m/%d/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def make_file_path_for_model(user_name):

    path = MEDIA_ROOT + '/upload/' + user_name + time.strftime("/%Y/%m/%d/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def handle_uploaded_file(f, user_name):

    file_name = unicode(f.name)

    path = MEDIA_ROOT + '/tmp/' + user_name + time.strftime("/%Y/%m/%d/")
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
    path = "/home/fangxu/djcode/ABE/key_info/1/cripto_info.txt"
    test = open(path, 'rb')
    a = test.publicKey
    print a