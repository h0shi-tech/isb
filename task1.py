# task1.py
import sys

# Алфавит
alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ "

# Функция для чтения файла
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Функция для записи в файл
def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

# Функция шифрования
def encrypt_text(text, key, alphabet):
    encrypted = ""
    for char in text:
        if char in alphabet:
            pos = alphabet.index(char)
            encrypted += key[pos]
        else:
            encrypted += char
    return encrypted

def main():
    # Проверка аргументов командной строки
    if len(sys.argv) != 4:
        print("Использование: python task1.py <input_file> <output_file> <key_file>")
        sys.exit(1)

    input_file = sys.argv[1]  # Путь к исходному файлу
    output_file = sys.argv[2]  # Путь к зашифрованному файлу
    key_file = sys.argv[3]    # Путь к файлу с ключом

    # Ключ шифрования
    key = "ЩЧЦХФУТСРПОНМЛКЙИЗЖЕДГВБАЮЭЫЬШЩЧЦ"

    # Чтение и обработка текста
    text = read_file(input_file).upper().replace("Е", " ")

    # Шифрование
    encrypted = encrypt_text(text, key, alphabet)

    # Сохранение результатов
    write_file(output_file, encrypted)
    write_file(key_file, key)

if __name__ == "__main__":
    main()