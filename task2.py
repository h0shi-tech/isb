"""
Модуль для дешифрования текста с помощью частотного анализа.
"""

from collections import Counter
from file_utils import read_text_file, write_text_file, write_json_file
from config import TASK2_CONFIG

def calculate_frequencies(text: str) -> dict:
    """
    Подсчет частот символов в тексте.

    Args:
        text (str): Текст для анализа.

    Returns:
        dict: Словарь с частотами символов.
    """
    frequencies = Counter(text)
    total_chars = len(text)
    return {char: count/total_chars for char, count in frequencies.items()}

def create_frequency_mapping(cipher_freq: dict, russian_freq: dict) -> dict:
    """
    Создание mapping на основе частот символов.

    Args:
        cipher_freq (dict): Частоты символов в зашифрованном тексте.
        russian_freq (dict): Частоты символов в русском языке.

    Returns:
        dict: Mapping для дешифрования.
    """
    # Сортировка по убыванию частоты
    sorted_cipher_freq = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_russian_freq = sorted(russian_freq.items(), key=lambda x: x[1], reverse=True)

    # Создание mapping
    mapping = {}
    for (cipher_char, _), (rus_char, _) in zip(sorted_cipher_freq, sorted_russian_freq):
        if cipher_char not in ['\n', 'l', 'I']:  # Пропускаем лишние символы
            mapping[cipher_char] = rus_char
    return mapping

def decrypt_text(text: str, mapping: dict) -> str:
    """
    Дешифрование текста с помощью mapping.

    Args:
        text (str): Зашифрованный текст.
        mapping (dict): Mapping для дешифрования.

    Returns:
        str: Расшифрованный текст.
    """
    decrypted = ""
    for char in text:
        if char in mapping:
            decrypted += mapping[char]
        else:
            decrypted += char
    return decrypted

def main():
    """Основная функция для выполнения дешифрования."""
    try:
        # Чтение зашифрованного текста
        cipher_text = read_text_file(TASK2_CONFIG["input_file"])
        
        # Подсчет частот
        cipher_freq = calculate_frequencies(cipher_text)
        
        # Создание mapping
        mapping = create_frequency_mapping(
            cipher_freq,
            TASK2_CONFIG["russian_freq"]
        )
        
        # Дешифрование
        decrypted = decrypt_text(cipher_text, mapping)
        
        # Сохранение результатов
        write_text_file(TASK2_CONFIG["decrypted_output"], decrypted)
        write_json_file(TASK2_CONFIG["key_output"], mapping)
        
        print("Дешифрование успешно завершено")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main() 