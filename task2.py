# task2.py
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

# Чтение зашифрованного текста
with open("cod15.txt", "r", encoding="utf-8") as f:
    cipher_text = f.read()

# Подсчёт частот символов в зашифрованном тексте
frequencies = Counter(cipher_text)
total_chars = len(cipher_text)
cipher_freq = {char: count/total_chars for char, count in frequencies.items()}

# Сортировка по убыванию частоты
sorted_cipher_freq = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
sorted_russian_freq = sorted(russian_freq.items(), key=lambda x: x[1], reverse=True)

# Создание mapping на основе частот
mapping = {}
for (cipher_char, _), (rus_char, _) in zip(sorted_cipher_freq, sorted_russian_freq):
    if cipher_char not in ['\n', 'l', 'I']:  # Пропускаем лишние символы
        mapping[cipher_char] = rus_char

# Расшифровка текста
decrypted = ""
for char in cipher_text:
    if char in mapping:
        decrypted += mapping[char]
    else:
        decrypted += char  # Оставляем символы, которые не сопоставлены

# Сохранение результатов
with open("task2_decrypted.txt", "w", encoding="utf-8") as f:
    f.write(decrypted)

# Сохранение ключа
with open("task2_key.txt", "w", encoding="utf-8") as f:
    f.write("Сопоставление символов (зашифрованный → расшифрованный):\n")
    for cipher_char, rus_char in mapping.items():
        f.write(f"{cipher_char} → {rus_char}\n")