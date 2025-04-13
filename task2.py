# task2.py
import json
from collections import Counter

def read_text_file(file_path):
    """Чтение текстового файла."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_text_file(file_path, content):
    """Запись содержимого в текстовый файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def write_json_file(file_path, data):
    """Запись данных в JSON файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def analyze_frequencies(text):
    """Анализ частотности символов в тексте."""
    frequencies = Counter(text)  # Подсчет частоты каждого символа
    total_chars = len(text)  # Общее количество символов
    return {char: count/total_chars for char, count in frequencies.items()}  # Вычисление относительной частоты

def create_mapping(cipher_freq, russian_freq):
    """Создание соответствия между символами шифра и русскими символами на основе частотности."""
    sorted_cipher = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)  # Сортировка символов шифра по частоте
    sorted_russian = sorted(russian_freq.items(), key=lambda x: x[1], reverse=True)  # Сортировка русских символов по частоте
    
    mapping = {}
    for (cipher_char, _), (rus_char, _) in zip(sorted_cipher, sorted_russian):
        if cipher_char not in ['\n', 'l', 'I']:  # Пропускаем специальные символы
            mapping[cipher_char] = rus_char
    return mapping

def decrypt_text(text, mapping):
    """Расшифровка текста с использованием соответствия символов."""
    return "".join(mapping.get(char, char) for char in text)  # Замена символов согласно соответствию

def main():
    # Конфигурация программы
    config = {
        "alphabet": "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ ",  # Русский алфавит
        "input_file": "cod15.txt",  # Зашифрованный файл
        "decrypted_output": "task2_decrypted.txt",  # Расшифрованный файл
        "key_output": "task2_key.json",  # Файл с ключом в формате JSON
        "russian_freq": {  # Частотность русских букв
            " ": 0.175, "О": 0.09, "Е": 0.072, "А": 0.062, "И": 0.062,
            "Н": 0.053, "Т": 0.053, "С": 0.045, "Р": 0.04, "В": 0.038,
            "Л": 0.035, "К": 0.028, "М": 0.026, "Д": 0.025, "П": 0.023,
            "У": 0.021, "Я": 0.018, "Ы": 0.016, "З": 0.016, "Б": 0.014,
            "Г": 0.013, "Ч": 0.012, "Й": 0.01, "Х": 0.009, "Ж": 0.007,
            "Ш": 0.006, "Ю": 0.006, "Ц": 0.004, "Щ": 0.003, "Э": 0.003,
            "Ф": 0.002, "Ъ": 0.001, "Ё": 0.001
        }
    }
    
    # Чтение зашифрованного текста
    cipher_text = read_text_file(config["input_file"])
    
    # Анализ частотности символов
    cipher_freq = analyze_frequencies(cipher_text)
    
    # Создание соответствия символов
    mapping = create_mapping(cipher_freq, config["russian_freq"])
    
    # Расшифровка текста
    decrypted = decrypt_text(cipher_text, mapping)
    
    # Сохранение результатов
    write_text_file(config["decrypted_output"], decrypted)
    write_json_file(config["key_output"], mapping)

if __name__ == "__main__":
    main()