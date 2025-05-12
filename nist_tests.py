import math
import numpy as np
from typing import List, Dict
import json
import os

# Константы из документации NIST
BLOCK_SIZE = 8  # Размер блока для теста на самую длинную последовательность единиц
EXPECTED_VALUES = [0.2148, 0.3672, 0.2305, 0.1875]  # Ожидаемые значения для размера блока 8
SIGNIFICANCE_LEVEL = 0.01  # Стандартный уровень значимости для тестов NIST

def read_sequence(filename: str) -> List[int]:
    """
    Читает бинарную последовательность из файла.
    
    Args:
        filename: Путь к файлу, содержащему бинарную последовательность
        
    Returns:
        Список целых чисел (0 и 1), представляющих последовательность
        
    Raises:
        FileNotFoundError: Если указанный файл не существует
        ValueError: Если файл содержит недопустимые символы
    """
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if not all(bit in '01' for bit in content):
                raise ValueError("Файл содержит недопустимые символы. Разрешены только 0 и 1.")
            return [int(bit) for bit in content]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла {filename}: {str(e)}")

def frequency_test(sequence: List[int]) -> float:
    """
    Выполняет частотный (монобитный) тест на бинарной последовательности.
    
    Этот тест определяет, соответствует ли количество 0 и 1 в последовательности
    ожидаемому для действительно случайной последовательности.
    
    Args:
        sequence: Список целых чисел (0 и 1) для тестирования
        
    Returns:
        p-значение теста
    """
    n = len(sequence)
    s = sum(2 * bit - 1 for bit in sequence)
    s_obs = abs(s) / math.sqrt(n)
    return math.erfc(s_obs / math.sqrt(2))

def runs_test(sequence: List[int]) -> float:
    """
    Выполняет тест на серии одинаковых битов.
    
    Этот тест определяет, соответствует ли количество серий единиц и нулей
    различной длины ожидаемому для случайной последовательности.
    
    Args:
        sequence: Список целых чисел (0 и 1) для тестирования
        
    Returns:
        p-значение теста
    """
    n = len(sequence)
    pi = sum(sequence) / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    v = 0  # Начинаем с 0, считаем переходы
    for i in range(1, n):
        if sequence[i] != sequence[i-1]:
            v += 1

    return math.erfc(abs(v - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi)))

def longest_run_ones_test(sequence: List[int]) -> float:
    """
    Выполняет тест на самую длинную последовательность единиц.
    
    Этот тест определяет, соответствует ли длина самой длинной серии единиц
    в тестируемой последовательности ожидаемой для случайной последовательности.
    
    Args:
        sequence: Список целых чисел (0 и 1) для тестирования
        
    Returns:
        p-значение теста
    """
    n = len(sequence)
    num_blocks = n // BLOCK_SIZE
    
    if num_blocks < 1:
        return 0.0

    # Находим максимальную длину серии единиц в каждом блоке
    max_runs = []
    for i in range(num_blocks):
        block = sequence[i * BLOCK_SIZE : (i + 1) * BLOCK_SIZE]
        current_run = max_run = 0
        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        max_runs.append(max_run)

    # Подсчитываем серии в каждой категории
    counts = [0] * len(EXPECTED_VALUES)
    for run in max_runs:
        if run <= 1:
            counts[0] += 1
        elif run == 2:
            counts[1] += 1
        elif run == 3:
            counts[2] += 1
        else:
            counts[3] += 1

    # Вычисляем статистику хи-квадрат
    chi_square = sum((obs - num_blocks * exp) ** 2 / (num_blocks * exp) 
                    for obs, exp in zip(counts, EXPECTED_VALUES))
    
    # Вычисляем p-значение с помощью неполной гамма-функции
    return math.gamma(2.5) * math.exp(-chi_square/2) * (chi_square/2) ** 1.5

def test_sequence(filename: str) -> Dict[str, float]:
    """
    Тестирует бинарную последовательность с помощью всех статистических тестов NIST.
    
    Args:
        filename: Путь к файлу, содержащему бинарную последовательность
        
    Returns:
        Словарь, содержащий названия тестов и их p-значения
    """
    sequence = read_sequence(filename)
    
    results = {
        "Частотный побитовый тест": frequency_test(sequence),
        "Тест на одинаковые подряд идущие биты": runs_test(sequence),
        "Тест на самую длинную последовательность единиц": longest_run_ones_test(sequence)
    }
    
    print(f"\nРезультаты тестов NIST для {filename}:")
    for test_name, p_value in results.items():
        print(f"{test_name}: p-value = {p_value}")
    print()
    
    return results

def main():
    """Основная функция для запуска тестов NIST на случайных последовательностях."""
    try:
        # Тестируем последовательности из обоих генераторов
        test_sequence("part1/random_sequence.txt")
        test_sequence("part2/random_sequence_java.txt")
    except Exception as e:
        print(f"Ошибка при тестировании: {str(e)}")

if __name__ == "__main__":
    main() 
