import argparse
from symmetric_crypto import SymmetricCrypto
from asymmetric_crypto import AsymmetricCrypto
import utils

def generate_keys(symmetric_key_path, public_key_path, private_key_path):
    """Сценарий 1: Генерация ключей"""
    print("Генерация ключей...")
    
    # Генерация ключей
    sym_crypto = SymmetricCrypto()
    asym_crypto = AsymmetricCrypto()
    
    symmetric_key = sym_crypto.generate_key()
    private_key, public_key = asym_crypto.generate_keys()
    
    # Сохранение ключей
    utils.save_public_key(public_key, public_key_path)
    utils.save_private_key(private_key, private_key_path)
    
    # Шифрование и сохранение симметричного ключа
    encrypted_symmetric_key = asym_crypto.encrypt(symmetric_key)
    utils.save_data(encrypted_symmetric_key, symmetric_key_path)
    
    print("Ключи успешно сгенерированы и сохранены")

def encrypt_file(input_file, private_key_path, symmetric_key_path, output_file):
    """Сценарий 2: Шифрование файла"""
    print("Начало шифрования файла...")
    
    # Загрузка ключей
    private_key = utils.load_private_key(private_key_path)
    encrypted_symmetric_key = utils.load_data(symmetric_key_path)
    
    # Инициализация криптосистем
    asym_crypto = AsymmetricCrypto()
    asym_crypto.private_key = private_key
    
    sym_crypto = SymmetricCrypto()
    sym_crypto.key = asym_crypto.decrypt(encrypted_symmetric_key)
    sym_crypto.generate_iv()
    
    # Шифрование данных
    data = utils.load_data(input_file)
    encrypted_data = sym_crypto.encrypt(data)
    
    # Сохранение зашифрованных данных с IV
    utils.save_data(sym_crypto.iv + encrypted_data, output_file)
    
    print("Файл успешно зашифрован")

def decrypt_file(input_file, private_key_path, symmetric_key_path, output_file):
    """Сценарий 3: Дешифрование файла"""
    print("Начало дешифрования файла...")
    
    # Загрузка ключей
    private_key = utils.load_private_key(private_key_path)
    encrypted_symmetric_key = utils.load_data(symmetric_key_path)
    
    # Инициализация криптосистем
    asym_crypto = AsymmetricCrypto()
    asym_crypto.private_key = private_key
    
    sym_crypto = SymmetricCrypto()
    sym_crypto.key = asym_crypto.decrypt(encrypted_symmetric_key)
    
    # Загрузка и разделение данных
    data = utils.load_data(input_file)
    sym_crypto.iv = data[:16]
    encrypted_data = data[16:]
    
    # Дешифрование данных
    decrypted_data = sym_crypto.decrypt(encrypted_data)
    
    # Сохранение расшифрованных данных
    utils.save_data(decrypted_data, output_file)
    
    print("Файл успешно расшифрован")

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
    
    if args.generate:
        if not all([args.symmetric_key, args.public_key, args.private_key]):
            parser.error("Для режима генерации ключей необходимо указать все пути для сохранения ключей")
        generate_keys(args.symmetric_key, args.public_key, args.private_key)
    
    elif args.encrypt:
        if not all([args.input, args.output, args.private_key, args.symmetric_key]):
            parser.error("Для режима шифрования необходимо указать все необходимые пути")
        encrypt_file(args.input, args.private_key, args.symmetric_key, args.output)
    
    elif args.decrypt:
        if not all([args.input, args.output, args.private_key, args.symmetric_key]):
            parser.error("Для режима дешифрования необходимо указать все необходимые пути")
        decrypt_file(args.input, args.private_key, args.symmetric_key, args.output)

if __name__ == "__main__":
    main() 
