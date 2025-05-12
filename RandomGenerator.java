import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.ArrayList;
import java.util.List;

/**
 * Класс для генерации псевдослучайных последовательностей.
 * Использует стандартный генератор случайных чисел Java.
 */
public class RandomGenerator {
    /**
     * Генерирует псевдослучайную последовательность заданной длины.
     *
     * @param length длина генерируемой последовательности в битах
     * @return список булевых значений, представляющих последовательность
     */
    public static List<Boolean> generateRandomSequence(int length) {
        List<Boolean> sequence = new ArrayList<>();
        Random random = new Random();

        for (int i = 0; i < length; i++) {
            sequence.add(random.nextBoolean());
        }

        return sequence;
    }

    /**
     * Основной метод программы.
     * Генерирует последовательность длиной 1 миллион бит и сохраняет её в файл.
     *
     * @param args аргументы командной строки (не используются)
     */
    public static void main(String[] args) {
        // Генерация последовательности
        int sequenceLength = 1000000; // 1 миллион бит
        List<Boolean> sequence = generateRandomSequence(sequenceLength);

        // Сохранение последовательности в файл
        try (FileWriter writer = new FileWriter("random_sequence_java.txt")) {
            for (boolean bit : sequence) {
                writer.write(bit ? "1" : "0");
            }
            System.out.println("Последовательность сгенерирована и сохранена в файл random_sequence_java.txt");
        } catch (IOException e) {
            System.err.println("Ошибка при записи в файл: " + e.getMessage());
        }
    }
} 
