import json

def save_card_number(card_number):
    """
    Сохраняет найденный номер карты в JSON файл.
    
    Аргументы:
        card_number (str): Найденный номер карты для сохранения
    """
    with open('card_number.json', 'w') as f:
        json.dump({"card_number": card_number}, f) 