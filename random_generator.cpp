#include <iostream>
#include <fstream>
#include <random>
#include <vector>

/**
 * @brief Генератор псевдослучайных последовательностей на C++
 * 
 * Программа генерирует последовательность случайных битов длиной 1 миллион
 * с помощью генератора Mersenne Twister и сохраняет её в файл.
 * 
 * @return int 0 при успешном выполнении, 1 при ошибке
 */
int main() {
    // Инициализация генератора случайных чисел
    std::random_device rd;  // Источник энтропии
    std::mt19937 gen(rd()); // Генератор Mersenne Twister
    std::bernoulli_distribution d(0.5); // Распределение Бернулли с p=0.5

    // Генерация 1 миллиона бит
    const int sequenceLength = 1000000;
    std::vector<bool> sequence;
    sequence.reserve(sequenceLength);

    for (int i = 0; i < sequenceLength; i++) {
        sequence.push_back(d(gen));
    }

    // Сохранение последовательности в файл
    std::ofstream outFile("random_sequence.txt");
    if (!outFile) {
        std::cerr << "Ошибка при открытии файла" << std::endl;
        return 1;
    }

    for (bool bit : sequence) {
        outFile << bit;
    }
    outFile.close();

    std::cout << "Последовательность сгенерирована и сохранена в файл random_sequence.txt" << std::endl;
    return 0;
} 
