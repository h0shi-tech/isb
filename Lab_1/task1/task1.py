# task1.py
alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ "  # Алфавит
key = "ЩЧЦХФУТСРПОНМЛКЙИЗЖЕДГВБАЮЭЫЬШЩЧЦ"  # Пример ключа
text = open("task1_original.txt", "r", encoding="utf-8").read().upper().replace("Е", " ")

encrypted = ""
for char in text:
    if char in alphabet:
        pos = alphabet.index(char)  # Находим позицию символа
        encrypted += key[pos]  # Заменяем на символ из ключа
    else:
        encrypted += char  # Оставляем другие символы без изменений

with open("task1_encrypted.txt", "w", encoding="utf-8") as f:
    f.write(encrypted)
with open("task1_key.txt", "w", encoding="utf-8") as f:
    f.write(key)