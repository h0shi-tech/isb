# task2.py
alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ "  # Алфавит
cipher_text = open("cod15.txt", "r", encoding="utf-8").read()

# Предположим частотное сопоставление: "2" -> " ", "А" -> "О", "П" -> "И" и т.д.
mapping = {
    "2": " ",
    "А": "О",
    "П": "И",
    "Ю": "Е",
    "Х": "Т",
    # Добавить остальные сопоставления на основе анализа
}

decrypted = ""
for char in cipher_text:
    decrypted += mapping.get(char, char)  # Заменяем, если есть соответствие

# Сохранение результатов
with open("task2_decrypted.txt", "w", encoding="utf-8") as f:
    f.write(decrypted)
with open("task2_key.txt", "w", encoding="utf-8") as f:
    f.write(str(mapping))  # Сохраняем словарь как ключ