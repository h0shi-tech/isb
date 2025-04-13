# task1.py
import json
import os

def read_text_file(file_path):
    """Чтение и обработка текстового файла."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().upper().replace("Е", " ")

def write_text_file(file_path, content):
    """Запись содержимого в текстовый файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def write_json_file(file_path, data):
    """Запись данных в JSON файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def encrypt_text(text, alphabet, key):
    """Шифрование текста с помощью подстановочного шифра."""
    encrypted = ""
    for char in text:
        if char in alphabet:
            pos = alphabet.index(char)  # Находим позицию символа в алфавите
            encrypted += key[pos]  # Заменяем на символ из ключа
        else:
            encrypted += char  # Оставляем другие символы без изменений
    return encrypted

def main():
    # Конфигурация программы
    config = {
        "alphabet": "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ ",  # Русский алфавит
        "key": "ЩЧЦХФУТСРПОНМЛКЙИЗЖЕДГВБАЮЭЫЬШЩЧЦ",  # Ключ шифрования
        "input_file": "task1_original.txt",  # Исходный файл
        "encrypted_output": "task1_encrypted.txt",  # Зашифрованный файл
        "key_output": "task1_key.json"  # Файл с ключом в формате JSON
    }
    
    # Чтение и обработка входного файла
    text = read_text_file(config["input_file"])
    
    # Шифрование текста
    encrypted = encrypt_text(text, config["alphabet"], config["key"])
    
    # Сохранение результатов
    write_text_file(config["encrypted_output"], encrypted)
    write_json_file(config["key_output"], {
        "alphabet": config["alphabet"],
        "key": config["key"]
    })

if __name__ == "__main__":
    main()