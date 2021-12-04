import base64

from Crypto.Cipher import AES
from Crypto.Util.py3compat import bchr, bord

from app import get_settings


class AESCipher(object):
    block_size = AES.block_size
    settings = get_settings()

    @classmethod
    def encrypt(cls, data):
        if isinstance(data, str):
            data = data.encode()
        else:
            data = str(data).encode()
        data = cls.pad(data)
        cipher = AES.new(
            key=cls.settings.encryption_key, mode=AES.MODE_CBC, IV=cls.settings.encryption_salt
        )
        encrypted_data = cipher.encrypt(data)
        encrypted_data = base64.b64encode(encrypted_data)
        encrypted_data = encrypted_data.decode(errors='ignore')
        return encrypted_data

    @classmethod
    def decrypt(cls, encrypted_data):
        encrypted_data = base64.b64decode(encrypted_data)
        cipher = AES.new(
            key=cls.settings.secret_key, mode=cls.settings.encryption_mode, IV=cls.settings.encryption_salt
        )
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
