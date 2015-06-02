import time
import os
from django.core.files import File
from tree import tree
from ABE.settings import MEDIA_ROOT
from cripto import Crypto
from decrypto import deCrypto
from file_key_process import share_to_attr, generator_tree_for_user
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import pickle


def generator_key_for_user(user, user_id, file_id):
    path = BASE_DIR + '/key_info/' + str(user_id) + '/' + 'cripto_info.txt'
    cry = Crypto(400, "username")
    key_info = open(path, 'rb')
    key_file = pickle.load(key_info)
    cry.publicKey = key_file['publicKey']
    cry.masterkey = key_file['masterKey']
    cry.attributi = key_file['attributi']
    cry.keygenerator = key_file['keygenerator']
    key_info.close()
    path_in_file = BASE_DIR + '/file_key/' + str(file_id)
    tree_of_user = generator_tree_for_user(user)
    in_file = open(path_in_file, 'rb')
    key_list = pickle.load(in_file)
    privatekey = cry.keygenerator.keygen(tree_of_user)
    key = ''
    for E in key_list:
        decry = deCrypto(tree_of_user, privatekey)
        key += chr(decry.decifra(E, privatekey))
    return key


def generator_key_for_user_self(user, file_id):
    path = BASE_DIR + '/key_info/' + str(user.id) + '/' + 'cripto_info.txt'
    cry = Crypto(400, "username")
    key_info = open(path, 'rb')
    key_file = pickle.load(key_info)
    cry.publicKey = key_file['publicKey']
    cry.masterkey = key_file['masterKey']
    cry.attributi = key_file['attributi']
    cry.keygenerator = key_file['keygenerator']
    key_info.close()
    path_in_file = BASE_DIR + '/file_key/' + (str(file_id) + "_self")
    tree_of_user = generator_tree_for_user(user)
    in_file = open(path_in_file, 'rb')
    key_list = pickle.load(in_file)
    privatekey = cry.keygenerator.keygen(tree_of_user)
    key = ''
    for E in key_list:
        decry = deCrypto(tree_of_user, privatekey)
        key += chr(decry.decifra(E, privatekey))
    return key


def delete_file_key(file_id, type):
    if type == '2':
        path_out = BASE_DIR + '/file_key/'
        path_out += (str(file_id) + "_self")
        delete_file(path_out)
        path_out = BASE_DIR + '/file_key/'
        path_out += str(file_id)
        return delete_file(path_out)
    if type == '3':
        path_out = BASE_DIR + '/file_key/'
        path_out += (str(file_id) + "_self")
        return delete_file(path_out)
    return True


def file_key_encrypt(user, file_id, share, key, type):
    path = BASE_DIR + '/key_info/' + str(user.id) + '/' + 'cripto_info.txt'
    cry = Crypto(400, "username")
    key_info = open(path, 'rb')
    key_file = pickle.load(key_info)
    cry.publicKey = key_file['publicKey']
    cry.masterkey = key_file['masterKey']
    cry.attributi = key_file['attributi']
    cry.keygenerator = key_file['keygenerator']
    key_info.close()
    # generate key for other user
    if type == 2:
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
    #generate key for user self
    attr = [int(user.dataofuser.sex), int(user.dataofuser.identity), int(user.dataofuser.academy_id)+10, int(user.dataofuser.major_id)+50]
    key_list = []
    for mess in key:
        E = cry.encrypto(ord(mess), attr)
        key_list.append(E)
    path_out = BASE_DIR + '/file_key/'
    path_out += (str(file_id) + "_self")
    file_out = open(path_out, 'wb')
    pickle.dump(key_list, file_out)
    file_out.close()

def set_user_abe_key_path(user_id):
    path = BASE_DIR + '/key_info/' + user_id + '/'
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