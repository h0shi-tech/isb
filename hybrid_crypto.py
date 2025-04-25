import os
import argparse
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding

class HybridCryptoSystem:
    def __init__(self):
        self.symmetric_key = None
        self.private_key = None
        self.public_key = None
        self.iv = None

    def generate_keys(self, symmetric_key_path, public_key_path, private_key_path):
        """Генерация ключей гибридной системы"""
        print("Генерация ключей...")
        
        # Генерация ключа для SEED (128 бит)
        self.symmetric_key = os.urandom(16)  # 128 бит = 16 байт
        print("Сгенерирован ключ для SEED")

        # Генерация ключей RSA
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        print("Сгенерированы ключи RSA")

        # Сохранение открытого ключа
        with open(public_key_path, 'wb') as public_out:
            public_out.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        print(f"Открытый ключ сохранен в {public_key_path}")

        # Сохранение закрытого ключа
        with open(private_key_path, 'wb') as private_out:
            private_out.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        print(f"Закрытый ключ сохранен в {private_key_path}")

        # Шифрование и сохранение симметричного ключа
        encrypted_symmetric_key = self.public_key.encrypt(
            self.symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        with open(symmetric_key_path, 'wb') as key_file:
            key_file.write(encrypted_symmetric_key)
        print(f"Зашифрованный симметричный ключ сохранен в {symmetric_key_path}")

    def encrypt_file(self, input_file, private_key_path, symmetric_key_path, output_file):
        """Шифрование файла гибридной системой"""
        print("Начало шифрования файла...")

        # Загрузка закрытого ключа
        with open(private_key_path, 'rb') as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        print("Закрытый ключ загружен")

        # Загрузка и расшифровка симметричного ключа
        with open(symmetric_key_path, 'rb') as key_file:
            encrypted_symmetric_key = key_file.read()
        self.symmetric_key = self.private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ расшифрован")

        # Генерация IV для SEED
        self.iv = os.urandom(16)
        print("Сгенерирован IV для SEED")

        # Чтение входного файла
        with open(input_file, 'rb') as file:
            data = file.read()
        print(f"Прочитан входной файл: {input_file}")

        # Паддинг данных
        padder = sym_padding.ANSIX923(16).padder()
        padded_data = padder.update(data) + padder.finalize()
        print("Данные дополнены паддингом")

        # Шифрование данных
        cipher = Cipher(algorithms.SEED(self.symmetric_key), modes.CBC(self.iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        print("Данные зашифрованы алгоритмом SEED")

        # Сохранение зашифрованных данных вместе с IV
        with open(output_file, 'wb') as file:
            file.write(self.iv + encrypted_data)
        print(f"Зашифрованные данные сохранены в {output_file}")

    def decrypt_file(self, input_file, private_key_path, symmetric_key_path, output_file):
        """Дешифрование файла гибридной системой"""
        print("Начало дешифрования файла...")

        # Загрузка закрытого ключа
        with open(private_key_path, 'rb') as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        print("Закрытый ключ загружен")

        # Загрузка и расшифровка симметричного ключа
        with open(symmetric_key_path, 'rb') as key_file:
            encrypted_symmetric_key = key_file.read()
        self.symmetric_key = self.private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ расшифрован")

        # Чтение зашифрованных данных
        with open(input_file, 'rb') as file:
            data = file.read()
        print(f"Прочитан зашифрованный файл: {input_file}")

        # Извлечение IV и зашифрованных данных
        self.iv = data[:16]
        encrypted_data = data[16:]
        print("Извлечен IV")

        # Дешифрование данных
        cipher = Cipher(algorithms.SEED(self.symmetric_key), modes.CBC(self.iv))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        print("Данные расшифрованы алгоритмом SEED")

        # Удаление паддинга
        unpadder = sym_padding.ANSIX923(16).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        print("Удален паддинг")

        # Сохранение расшифрованных данных
        with open(output_file, 'wb') as file:
            file.write(unpadded_data)
        print(f"Расшифрованные данные сохранены в {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Гибридная криптосистема (RSA + SEED)')
    group = parser.add_mutually_exclusive_group(required=True)
    
    # Режим генерации ключей
    group.add_argument('-gen', '--generate', action='store_true',
                      help='Запускает режим генерации ключей')
    parser.add_argument('-sk', '--symmetric-key', help='Путь для сохранения зашифрованного симметричного ключа')
    parser.add_argument('-pub', '--public-key', help='Путь для сохранения открытого ключа')
    parser.add_argument('-priv', '--private-key', help='Путь для сохранения закрытого ключа')
    
    # Режим шифрования
    group.add_argument('-enc', '--encrypt', action='store_true',
                      help='Запускает режим шифрования')
    parser.add_argument('-in', '--input', help='Путь к входному файлу')
    parser.add_argument('-out', '--output', help='Путь для сохранения выходного файла')
    
    # Режим дешифрования
    group.add_argument('-dec', '--decrypt', action='store_true',
                      help='Запускает режим дешифрования')
    
    args = parser.parse_args()
    
    crypto_system = HybridCryptoSystem()
    
    if args.generate:
        if not all([args.symmetric_key, args.public_key, args.private_key]):
            parser.error("Для режима генерации ключей необходимо указать все пути для сохранения ключей")
        crypto_system.generate_keys(args.symmetric_key, args.public_key, args.private_key)
    
    elif args.encrypt:
        if not all([args.input, args.output, args.private_key, args.symmetric_key]):
            parser.error("Для режима шифрования необходимо указать все необходимые пути")
        crypto_system.encrypt_file(args.input, args.private_key, args.symmetric_key, args.output)
    
    elif args.decrypt:
        if not all([args.input, args.output, args.private_key, args.symmetric_key]):
            parser.error("Для режима дешифрования необходимо указать все необходимые пути")
        crypto_system.decrypt_file(args.input, args.private_key, args.symmetric_key, args.output)

if __name__ == "__main__":
    main() 