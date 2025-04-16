import math
import numpy as np

def read_sequence(filename):
    """Читает последовательность из файла и возвращает список битов"""
    with open(filename, 'r') as f:
        sequence = [int(bit) for bit in f.read().strip()]
    return sequence

def frequency_test(sequence):
    """Частотный побитовый тест"""
    n = len(sequence)
    s = sum(2 * bit - 1 for bit in sequence)
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

def runs_test(sequence):
    """Тест на одинаковые подряд идущие биты"""
    n = len(sequence)
    pi = sum(sequence) / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    v = 1  # Начинаем с 1, так как считаем и первый переход
    for i in range(1, n):
        if sequence[i] != sequence[i-1]:
            v += 1

    p_value = math.erfc(abs(v - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi)))
    return p_value

def longest_run_ones_test(sequence):
    """Тест на самую длинную последовательность единиц в блоке"""
    block_size = 128
    n = len(sequence)
    num_blocks = n // block_size
    
    if num_blocks < 1:
        return 0.0

    # Находим максимальную длину последовательности единиц в каждом блоке
    max_runs = []
    for i in range(num_blocks):
        block = sequence[i * block_size : (i + 1) * block_size]
        current_run = max_run = 0
        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        max_runs.append(max_run)

    # Таблица ожидаемых значений для blockSize = 128
    expected = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    counts = [0] * 6

    for run in max_runs:
        if run <= 4:
            counts[0] += 1
        elif run == 5:
            counts[1] += 1
        elif run == 6:
            counts[2] += 1
        elif run == 7:
            counts[3] += 1
        elif run == 8:
            counts[4] += 1
        else:
            counts[5] += 1

    chi_square = sum((obs - num_blocks * exp) ** 2 / (num_blocks * exp) 
                    for obs, exp in zip(counts, expected))
    p_value = 1 - chi2_cdf(chi_square, 5)
    return p_value

def chi2_cdf(x, df):
    """Функция распределения хи-квадрат"""
    return gammainc(x/2, df/2)

def gammainc(x, a):
    """Неполная гамма-функция"""
    return math.gamma(a) * math.exp(-x) * x ** (a-1)

def test_sequence(filename):
    """Тестирует последовательность всеми тестами"""
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

def main():
    # Тестируем последовательности из обоих генераторов
    test_sequence("part1/random_sequence.txt")
    test_sequence("part2/random_sequence_java.txt")

if __name__ == "__main__":
    main() 