import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.ArrayList;
import java.util.List;

public class RandomGenerator {
    // Функция для генерации псевдослучайной последовательности
    public static List<Boolean> generateRandomSequence(int length) {
        List<Boolean> sequence = new ArrayList<>();
        Random random = new Random();

        for (int i = 0; i < length; i++) {
            sequence.add(random.nextBoolean());
        }

        return sequence;
    }

    // 1. Частотный побитовый тест
    public static double frequencyTest(List<Boolean> sequence) {
        int sum = 0;
        for (boolean bit : sequence) {
            sum += bit ? 1 : -1;
        }
        double s = Math.abs(sum) / Math.sqrt(sequence.size());
        double p_value = erfc(s / Math.sqrt(2));
        return p_value;
    }

    // 2. Тест на одинаковые подряд идущие биты
    public static double runsTest(List<Boolean> sequence) {
        int n = sequence.size();
        double pi = 0;
        for (boolean bit : sequence) {
            pi += bit ? 1 : 0;
        }
        pi /= n;

        if (Math.abs(pi - 0.5) >= 2.0 / Math.sqrt(n)) {
            return 0.0;
        }

        int v = 1;
        for (int i = 1; i < n; i++) {
            if (sequence.get(i) != sequence.get(i-1)) {
                v++;
            }
        }

        double p_value = erfc(Math.abs(v - 2 * n * pi * (1 - pi)) / (2 * Math.sqrt(2 * n) * pi * (1 - pi)));
        return p_value;
    }

    // 3. Тест на самую длинную последовательность единиц в блоке
    public static double longestRunOfOnesTest(List<Boolean> sequence) {
        int blockSize = 128;
        int numBlocks = sequence.size() / blockSize;
        int[] maxRuns = new int[numBlocks];

        for (int i = 0; i < numBlocks; i++) {
            int currentRun = 0;
            int maxRun = 0;
            for (int j = 0; j < blockSize; j++) {
                if (sequence.get(i * blockSize + j)) {
                    currentRun++;
                    maxRun = Math.max(maxRun, currentRun);
                } else {
                    currentRun = 0;
                }
            }
            maxRuns[i] = maxRun;
        }

        // Таблица ожидаемых значений для blockSize = 128
        double[] expected = {0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124};
        int[] counts = new int[6];

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
            chi2 += Math.pow(counts[i] - numBlocks * expected[i], 2) / (numBlocks * expected[i]);
        }

        return 1 - chi2cdf(chi2, 5);
    }

    // Функция для вычисления CDF распределения хи-квадрат
    private static double chi2cdf(double x, int k) {
        return gammainc(x/2, k/2.0);
    }

    // Функция для вычисления неполной гамма-функции
    private static double gammainc(double x, double a) {
        double sum = 0;
        double term = 1;
        for (int n = 0; n < 100; n++) {
            sum += term;
            term *= x / (a + n + 1);
        }
        return sum * Math.pow(x, a) * Math.exp(-x) / gamma(a + 1);
    }

    // Функция для вычисления гамма-функции
    private static double gamma(double x) {
        double[] p = {0.99999999999980993, 676.5203681218851, -1259.1392167224028,
                     771.32342877765313, -176.61502916214059, 12.507343278686905,
                     -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7};
        int g = 7;
        if (x < 0.5) return Math.PI / (Math.sin(Math.PI * x) * gamma(1-x));
        x -= 1;
        double a = p[0];
        double t = x + g + 0.5;
        for (int i = 1; i < p.length; i++) {
            a += p[i] / (x + i);
        }
        return Math.sqrt(2 * Math.PI) * Math.pow(t, x + 0.5) * Math.exp(-t) * a;
    }

    // Функция для вычисления дополнительной функции ошибок
    private static double erfc(double x) {
        double z = Math.abs(x);
        double t = 1.0 / (1.0 + 0.5 * z);
        double ans = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 +
                t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 +
                t * (-0.82215223 + t * 0.17087277)))))))));
        return x >= 0 ? ans : 2 - ans;
    }

    public static void main(String[] args) {
        // Генерация последовательности
        int sequenceLength = 1000000; // 1 миллион бит
        List<Boolean> sequence = generateRandomSequence(sequenceLength);

        // Сохранение последовательности в файл
        try (FileWriter writer = new FileWriter("random_sequence_java.txt")) {
            for (boolean bit : sequence) {
                writer.write(bit ? "1" : "0");
            }
        } catch (IOException e) {
            System.err.println("Ошибка при записи в файл: " + e.getMessage());
        }

        // Выполнение тестов
        double freqTest = frequencyTest(sequence);
        double runsTestResult = runsTest(sequence);
        double longestRunTest = longestRunOfOnesTest(sequence);

        // Вывод результатов
        System.out.println("Результаты тестов NIST:");
        System.out.println("1. Частотный побитовый тест: p-value = " + freqTest);
        System.out.println("2. Тест на одинаковые подряд идущие биты: p-value = " + runsTestResult);
        System.out.println("3. Тест на самую длинную последовательность единиц: p-value = " + longestRunTest);
    }
} 