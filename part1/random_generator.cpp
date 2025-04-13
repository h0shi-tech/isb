#include <iostream>
#include <fstream>
#include <random>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

// Функция для вычисления гамма-функции
double gamma(double x) {
    const double p[] = {0.99999999999980993, 676.5203681218851, -1259.1392167224028,
                 771.32342877765313, -176.61502916214059, 12.507343278686905,
                 -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7};
    const int g = 7;
    if (x < 0.5) return M_PI / (sin(M_PI * x) * gamma(1-x));
    x -= 1;
    double a = p[0];
    double t = x + g + 0.5;
    for (int i = 1; i < 9; i++) {
        a += p[i] / (x + i);
    }
    return sqrt(2 * M_PI) * pow(t, x + 0.5) * exp(-t) * a;
}

// Функция для вычисления неполной гамма-функции
double gammainc(double x, double a) {
    double sum = 0;
    double term = 1;
    for (int n = 0; n < 100; n++) {
        sum += term;
        term *= x / (a + n + 1);
    }
    return sum * pow(x, a) * exp(-x) / gamma(a + 1);
}

// Функция для вычисления CDF распределения хи-квадрат
double chi2cdf(double x, int k) {
    return gammainc(x/2, k/2.0);
}

// Функция для вычисления дополнительной функции ошибок
double erfc(double x) {
    double z = abs(x);
    double t = 1.0 / (1.0 + 0.5 * z);
    double ans = t * exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 +
            t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 +
            t * (-0.82215223 + t * 0.17087277)))))))));
    return x >= 0 ? ans : 2 - ans;
}

// Функция для генерации псевдослучайной последовательности
vector<bool> generateRandomSequence(int length) {
    vector<bool> sequence;
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1);

    for (int i = 0; i < length; i++) {
        sequence.push_back(dis(gen));
    }

    return sequence;
}

// 1. Частотный побитовый тест
double frequencyTest(const vector<bool>& sequence) {
    int sum = 0;
    for (bool bit : sequence) {
        sum += bit ? 1 : -1;
    }
    double s = abs(sum) / sqrt(sequence.size());
    double p_value = erfc(s / sqrt(2));
    return p_value;
}

// 2. Тест на одинаковые подряд идущие биты
double runsTest(const vector<bool>& sequence) {
    int n = sequence.size();
    double pi = 0;
    for (bool bit : sequence) {
        pi += bit;
    }
    pi /= n;

    if (abs(pi - 0.5) >= 2.0 / sqrt(n)) {
        return 0.0;
    }

    int v = 1;
    for (int i = 1; i < n; i++) {
        if (sequence[i] != sequence[i-1]) {
            v++;
        }
    }

    double p_value = erfc(abs(v - 2 * n * pi * (1 - pi)) / (2 * sqrt(2 * n) * pi * (1 - pi)));
    return p_value;
}

// 3. Тест на самую длинную последовательность единиц в блоке
double longestRunOfOnesTest(const vector<bool>& sequence) {
    int blockSize = 128;
    int numBlocks = sequence.size() / blockSize;
    vector<int> maxRuns(numBlocks, 0);

    for (int i = 0; i < numBlocks; i++) {
        int currentRun = 0;
        int maxRun = 0;
        for (int j = 0; j < blockSize; j++) {
            if (sequence[i * blockSize + j]) {
                currentRun++;
                maxRun = max(maxRun, currentRun);
            } else {
                currentRun = 0;
            }
        }
        maxRuns[i] = maxRun;
    }

    // Таблица ожидаемых значений для blockSize = 128
    vector<double> expected = {0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124};
    vector<int> counts(6, 0);

    for (int run : maxRuns) {
        if (run <= 4) counts[0]++;
        else if (run == 5) counts[1]++;
        else if (run == 6) counts[2]++;
        else if (run == 7) counts[3]++;
        else if (run == 8) counts[4]++;
        else counts[5]++;
    }

    double chi2 = 0;
    for (int i = 0; i < 6; i++) {
        chi2 += pow(counts[i] - numBlocks * expected[i], 2) / (numBlocks * expected[i]);
    }

    return 1 - chi2cdf(chi2, 5);
}

int main() {
    // Генерация последовательности
    int sequenceLength = 1000000; // 1 миллион бит
    vector<bool> sequence = generateRandomSequence(sequenceLength);

    // Сохранение последовательности в файл
    ofstream outFile("random_sequence.txt");
    for (bool bit : sequence) {
        outFile << bit;
    }
    outFile.close();

    // Выполнение тестов
    double freqTest = frequencyTest(sequence);
    double runsTestResult = runsTest(sequence);
    double longestRunTest = longestRunOfOnesTest(sequence);

    // Вывод результатов
    cout << "Результаты тестов NIST:" << endl;
    cout << "1. Частотный побитовый тест: p-value = " << freqTest << endl;
    cout << "2. Тест на одинаковые подряд идущие биты: p-value = " << runsTestResult << endl;
    cout << "3. Тест на самую длинную последовательность единиц: p-value = " << longestRunTest << endl;

    return 0;
} 