from file_encryptor import convergence


def encrypt_file(path):
    key = convergence.encrypt_file_inline(path, None)
    return key


def decrypt_file(path, key):
    convergence.decrypt_file_inline(path, key)

if __name__ == '__main__':
    key = encrypt_file('./1.jpg')
    decrypt_file('./1.jpg', key)
    



