import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding

class SymmetricCrypto:
    def __init__(self):
        self.key = None
        self.iv = None

    def generate_key(self):
        """Генерация ключа для SEED (128 бит)"""
        self.key = os.urandom(16)  # 128 бит = 16 байт
        return self.key

    def generate_iv(self):
        """Генерация IV для SEED"""
        self.iv = os.urandom(16)
        return self.iv

    def encrypt(self, data):
        """Шифрование данных алгоритмом SEED"""
        # Паддинг данных
        padder = sym_padding.ANSIX923(16).padder()
        padded_data = padder.update(data) + padder.finalize()

        # Шифрование данных
        cipher = Cipher(algorithms.SEED(self.key), modes.CBC(self.iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return encrypted_data

    def decrypt(self, encrypted_data):
        """Дешифрование данных алгоритмом SEED"""
        # Дешифрование данных
        cipher = Cipher(algorithms.SEED(self.key), modes.CBC(self.iv))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Удаление паддинга
        unpadder = sym_padding.ANSIX923(16).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data 