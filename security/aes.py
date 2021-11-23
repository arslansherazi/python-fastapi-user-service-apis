import base64

from Crypto.Cipher import AES
from Crypto.Util.py3compat import bchr, bord

from security.credentials import ENCRYPTION_KEY, ENCRYPTION_MODE, ENCRYPTION_SALT


class AESCipher(object):
    block_size = AES.block_size

    @classmethod
    def encrypt(cls, data):
        data = cls.pad(data)
        cipher = AES.new(key=ENCRYPTION_KEY, mode=ENCRYPTION_MODE, IV=ENCRYPTION_SALT)
        encrypted_data = cipher.encrypt(data)
        encrypted_data = base64.b64encode(encrypted_data)
        encrypted_data = encrypted_data.decode(errors='ignore')
        return encrypted_data

    @classmethod
    def decrypt(cls, encrypted_data):
        encrypted_data = base64.b64decode(encrypted_data)
        cipher = AES.new(key=ENCRYPTION_KEY, mode=ENCRYPTION_MODE, IV=ENCRYPTION_SALT)
        data = cipher.decrypt(encrypted_data)
        data = cls.unpad(data)
        data = data.decode(errors='ignore')
        return data

    @classmethod
    def pad(cls, data):
        number_of_bytes_to_pad = cls.block_size - len(data) % cls.block_size
        padding = bchr(number_of_bytes_to_pad) * number_of_bytes_to_pad
        return data + padding

    @classmethod
    def unpad(cls, data):
        padding_len = bord(data[-1])
        return data[:-padding_len]
