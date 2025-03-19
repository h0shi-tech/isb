# task2.py
import sys
import json
from collections import Counter

# Алфавит
alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ "

# Частоты русского алфавита из методички
russian_freq = {
    " ": 0.128675, "О": 0.096456, "И": 0.075312, "Н": 0.061820, "Т": 0.061619,
    "С": 0.051953, "Е": 0.0461327, "Р": 0.040677, "А": 0.0381292, "В": 0.0321779,
    "Д": 0.0320343, "Л": 0.029803, "М": 0.029400, "П": 0.026983, "К": 0.025977,
    "У": 0.024768, "З": 0.0231484, "Г": 0.019108, "Б": 0.015908, "Я": 0.015707,
    "Ы": 0.015103, "Ч": 0.013290, "Ш": 0.011679, "Ж": 0.010673, "Ц": 0.008659,
    "Ю": 0.007249, "Э": 0.006847, "Х": 0.006645, "Щ": 0.005034, "Й": 0.004229,
    "Ь": 0.003625, "Ф": 0.002416, "Ъ": 0.000000
}

# Функция для чтения файла
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Функция для записи в файл
def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

# Функция для подсчёта частот символов
def calculate_frequencies(text):
    frequencies = Counter(text)
    total_chars = len(text)
    return {char: count/total_chars for char, count in frequencies.items()}

# Функция для создания mapping на основе частот
def create_mapping(cipher_freq, russian_freq):
    sorted_cipher_freq = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_russian_freq = sorted(russian_freq.items(), key=lambda x: x[1], reverse=True)
    mapping = {}
    for (cipher_char, _), (rus_char, _) in zip(sorted_cipher_freq, sorted_russian_freq):
        if cipher_char not in ['\n', 'l', 'I']:  # Пропускаем лишние символы
            mapping[cipher_char] = rus_char
    return mapping

# Функция для расшифровки текста
def decrypt_text(cipher_text, mapping):
    decrypted = ""
    for char in cipher_text:
        decrypted += mapping.get(char, char)  # Оставляем символы, которые не сопоставлены
    return decrypted

def main():
    # Проверка аргументов командной строки
    if len(sys.argv) != 4:
        print("Использование: python task2.py <input_file> <output_file> <key_file>")
        sys.exit(1)

    input_file = sys.argv[1]  # Путь к зашифрованному файлу
    output_file = sys.argv[2]  # Путь к расшифрованному файлу
    key_file = sys.argv[3]    # Путь к файлу с ключом (JSON)

    # Чтение зашифрованного текста
    cipher_text = read_file(input_file)

    # Подсчёт частот
    cipher_freq = calculate_frequencies(cipher_text)

    # Создание mapping
    mapping = create_mapping(cipher_freq, russian_freq)

    # Расшифровка текста
    decrypted = decrypt_text(cipher_text, mapping)

    # Сохранение результатов
    write_file(output_file, decrypted)

    # Сохранение mapping в JSON
    with open(key_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()