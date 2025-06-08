import multiprocessing as mp
import time
from tqdm import tqdm
from hash_utils import check_card, config

def check_card_wrapper(middle_digits):
    """
    Функция-обертка для multiprocessing.Pool.
    
    Аргументы:
        middle_digits (str): Средние 6 цифр номера карты
        
    Возвращает:
        str или None: Полный номер карты, если хеш совпадает, иначе None
    """
    return check_card(middle_digits, config["bin_codes"], config["last_four"], config["hash_to_find"])

def find_collision(processes):
    """
    Находит коллизию хеша для номера карты.
    
    Аргументы:
        processes (int): Количество используемых процессов
        
    Возвращает:
        tuple: (время выполнения в секундах, найденный номер карты или None)
    """
    start_time = time.time()
    middle_digits = [str(i).zfill(6) for i in range(1000000)]
    
    with mp.Pool(processes=processes) as pool:
        results = list(tqdm(pool.imap(check_card_wrapper, middle_digits), 
                          total=len(middle_digits), 
                          desc=f"Поиск с {processes} процессами"))
        
        for result in results:
            if result:
                pool.terminate()
                end_time = time.time()
                return end_time - start_time, result
                
    end_time = time.time()
    return end_time - start_time, None 