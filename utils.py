from cryptography.hazmat.primitives import serialization
import config

def save_public_key(public_key, path):
    """Сохранение открытого ключа
    
    Args:
        public_key: Объект открытого ключа
        path (str): Путь для сохранения открытого ключа
    """
    try:
        with open(path, 'wb') as public_out:
            public_out.write(public_key.public_bytes(
                encoding=config.get_serialization_encoding(),
                format=config.get_public_format()
            ))
    except Exception as e:
        print(f"Ошибка при сохранении открытого ключа: {str(e)}")
        raise

def save_private_key(private_key, path):
    """Сохранение закрытого ключа
    
    Args:
        private_key: Объект закрытого ключа
        path (str): Путь для сохранения закрытого ключа
    """
    try:
        with open(path, 'wb') as private_out:
            private_out.write(private_key.private_bytes(
                encoding=config.get_serialization_encoding(),
                format=config.get_private_format(),
                encryption_algorithm=config.get_encryption_algorithm()
            ))
    except Exception as e:
        print(f"Ошибка при сохранении закрытого ключа: {str(e)}")
        raise

def load_private_key(path):
    """Загрузка закрытого ключа
    
    Args:
        path (str): Путь к файлу с закрытым ключом
        
    Returns:
        Объект закрытого ключа
    """
    try:
        with open(path, 'rb') as key_file:
            return serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
    except Exception as e:
        print(f"Ошибка при загрузке закрытого ключа: {str(e)}")
        raise

def save_data(data, path):
    """Сохранение данных в файл
    
    Args:
        data (bytes): Данные для сохранения
        path (str): Путь для сохранения данных
    """
    try:
        with open(path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {str(e)}")
        raise

def load_data(path):
    """Загрузка данных из файла
    
    Args:
        path (str): Путь к файлу с данными
        
    Returns:
        bytes: Загруженные данные
    """
    try:
        with open(path, 'rb') as file:
            return file.read()
    except Exception as e:
        print(f"Ошибка при загрузке данных: {str(e)}")
        raise 
