import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_config():
    """Загрузка конфигурации из JSON файла"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке конфигурации: {str(e)}")
        raise

def get_serialization_encoding():
    """Получение параметров сериализации"""
    config = load_config()
    return getattr(serialization.Encoding, config['serialization']['encoding'])

def get_public_format():
    """Получение формата открытого ключа"""
    config = load_config()
    return getattr(serialization.PublicFormat, config['serialization']['public_format'])

def get_private_format():
    """Получение формата закрытого ключа"""
    config = load_config()
    return getattr(serialization.PrivateFormat, config['serialization']['private_format'])

def get_encryption_algorithm():
    """Получение алгоритма шифрования для закрытого ключа"""
    config = load_config()
    return getattr(serialization, config['serialization']['encryption_algorithm'])()

def get_rsa_padding():
    """Получение параметров паддинга RSA"""
    config = load_config()
    padding_config = config['asymmetric']['padding']
    return getattr(padding, padding_config['type'])(
        mgf=getattr(padding, padding_config['mgf'])(algorithm=getattr(hashes, padding_config['hash_algorithm'])()),
        algorithm=getattr(hashes, padding_config['hash_algorithm'])(),
        label=padding_config['label']
    ) 