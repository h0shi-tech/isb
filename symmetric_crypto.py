import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
import config

class SymmetricCrypto:
    def __init__(self):
        self.key = None
        self.iv = None

    def generate_key(self):
        """Генерация ключа для SEED"""
        config_data = config.load_config()
        self.key = os.urandom(config_data['symmetric']['key_size'])
        return self.key

    def generate_iv(self):
        """Генерация IV для SEED"""
        config_data = config.load_config()
        self.iv = os.urandom(config_data['symmetric']['iv_size'])
        return self.iv

    def encrypt(self, data):
        """Шифрование данных алгоритмом SEED"""
        config_data = config.load_config()
        
        
        padder = getattr(sym_padding, config_data['symmetric']['padding'])(config_data['symmetric']['block_size']).padder()
        padded_data = padder.update(data) + padder.finalize()

        
        cipher = Cipher(
            getattr(algorithms, config_data['symmetric']['algorithm'])(self.key),
            getattr(modes, config_data['symmetric']['mode'])(self.iv)
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return encrypted_data

    def decrypt(self, encrypted_data):
        """Дешифрование данных алгоритмом SEED"""
        config_data = config.load_config()
        
        
        cipher = Cipher(
            getattr(algorithms, config_data['symmetric']['algorithm'])(self.key),
            getattr(modes, config_data['symmetric']['mode'])(self.iv)
        )
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        
        unpadder = getattr(sym_padding, config_data['symmetric']['padding'])(config_data['symmetric']['block_size']).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data 
