import hashlib
import json

def load_config():
    """Загружает конфигурацию из файла config.json"""
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()

def check_card(middle_digits, bin_codes, last_four, hash_to_find):
    """
    Проверяет, соответствует ли номер карты с заданными средними цифрами целевому хешу.
    
    Аргументы:
        middle_digits (str): Средние 6 цифр номера карты
        bin_codes (list): Список действительных BIN-кодов
        last_four (str): Последние 4 цифры номера карты
        hash_to_find (str): Целевой хеш для сопоставления
        
    Возвращает:
        str или None: Полный номер карты, если хеш совпадает, иначе None
    """
    for bin_code in bin_codes:
        card_number = f"{bin_code}{middle_digits}{last_four}"
        if luhn_algorithm(card_number):
            card_hash = hashlib.sha224(card_number.encode()).hexdigest()
            if card_hash == hash_to_find:
                return card_number
    return None

def luhn_algorithm(card_number):
    """
    Реализует алгоритм Луна для проверки номера карты.
    
    Аргументы:
        card_number (str): 16-значный номер карты
        
    Возвращает:
        bool: True, если номер карты действителен, False в противном случае
    """
    digits = [int(d) for d in card_number]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(divmod(d * 2, 10))
    return checksum % 10 == 0 
