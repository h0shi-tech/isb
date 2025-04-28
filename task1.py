"""
Модуль для шифрования текста с помощью подстановочного шифра.
"""

from file_utils import read_text_file, write_text_file, write_json_file
from config import TASK1_CONFIG

def encrypt_text(text: str, alphabet: str, key: str) -> str:
    """
    Шифрование текста с помощью подстановочного шифра.

    Args:
        text (str): Исходный текст для шифрования.
        alphabet (str): Алфавит для шифрования.
        key (str): Ключ шифрования.

    Returns:
        str: Зашифрованный текст.
    """
    encrypted = ""
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            encrypted += key[index]
        else:
            encrypted += char
    return encrypted

def decrypt_text(text: str, alphabet: str, key: str) -> str:
    """
    Дешифрование текста с помощью подстановочного шифра.

    Args:
        text (str): Зашифрованный текст.
        alphabet (str): Алфавит для дешифрования.
        key (str): Ключ шифрования.

    Returns:
        str: Расшифрованный текст.
    """
    decrypted = ""
    for char in text:
        if char in key:
            index = key.index(char)
            decrypted += alphabet[index]
        else:
            decrypted += char
    return decrypted

def main():
    """Основная функция для выполнения шифрования."""
    try:
        # Чтение исходного текста
        text = read_text_file(TASK1_CONFIG["input_file"]).upper().replace("Е", " ")
        
        # Шифрование текста
        encrypted = encrypt_text(
            text,
            TASK1_CONFIG["alphabet"],
            TASK1_CONFIG["key"]
        )
        
        # Сохранение зашифрованного текста
        write_text_file(TASK1_CONFIG["encrypted_output"], encrypted)
        
        # Сохранение ключа в JSON
        key_data = {
            "alphabet": TASK1_CONFIG["alphabet"],
            "key": TASK1_CONFIG["key"]
        }
        write_json_file(TASK1_CONFIG["key_output"], key_data)
        
        print("Шифрование успешно завершено")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main() 