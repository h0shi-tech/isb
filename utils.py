from cryptography.hazmat.primitives import serialization

def save_public_key(public_key, path):
    """Сохранение открытого ключа"""
    with open(path, 'wb') as public_out:
        public_out.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def save_private_key(private_key, path):
    """Сохранение закрытого ключа"""
    with open(path, 'wb') as private_out:
        private_out.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def load_private_key(path):
    """Загрузка закрытого ключа"""
    with open(path, 'rb') as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

def save_data(data, path):
    """Сохранение данных в файл"""
    with open(path, 'wb') as file:
        file.write(data)

def load_data(path):
    """Загрузка данных из файла"""
    with open(path, 'rb') as file:
        return file.read() 