import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QMessageBox, QGroupBox)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from hash_utils import luhn_algorithm
from collision_finder import find_collision
from save_card import save_card_number
import multiprocessing as mp

class CollisionFinderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Поиск коллизий карт")
        self.setGeometry(300, 300, 500, 400)

        # Установить стили
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
            }
            QLabel {
                color: #333;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title = QLabel("Поиск коллизий карт")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(title)

        # Описание
        description = QLabel("Поиск коллизий хешей и проверка номера карты")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("color: #7f8c8d;")
        main_layout.addWidget(description)

        # Группа операций
        operations_group = QGroupBox("Операции")
        operations_layout = QVBoxLayout()
        operations_layout.setSpacing(10)

        self.find_button = QPushButton("Найти номер карты")
        self.find_button.clicked.connect(self.find_card)
        self.find_button.setToolTip("Найти действительный номер карты по заданному хешу")

        self.check_button = QPushButton("Проверить номер карты")
        self.check_button.clicked.connect(self.check_card)
        self.check_button.setToolTip("Проверить номер карты с использованием алгоритма Луна")

        self.measure_button = QPushButton("Измерить производительность")
        self.measure_button.clicked.connect(self.measure_time)
        self.measure_button.setToolTip("Измерить время поиска с разным количеством процессов")

        operations_layout.addWidget(self.find_button)
        operations_layout.addWidget(self.check_button)
        operations_layout.addWidget(self.measure_button)
        operations_group.setLayout(operations_layout)
        main_layout.addWidget(operations_group)

        # Группа проверки карты
        check_group = QGroupBox("Проверка карты")
        check_layout = QVBoxLayout()

        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("Введите 16-значный номер карты...")
        self.card_input.setMaxLength(16)
        self.card_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{16}")))

        check_layout.addWidget(self.card_input)
        check_group.setLayout(check_layout)
        main_layout.addWidget(check_group)

        # Строка состояния
        self.status_bar = QLabel()
        self.status_bar.setAlignment(Qt.AlignCenter)
        self.status_bar.setStyleSheet("color: #7f8c8d; font-style: italic;")
        main_layout.addWidget(self.status_bar)

        self.setLayout(main_layout)

    def find_card(self):
        self.status_bar.setText("Поиск номера карты...")
        QApplication.processEvents()

        processes = mp.cpu_count()
        time_taken, found_card = find_collision(processes)

        if found_card:
            save_card_number(found_card)
            self.status_bar.setText(f"Найден номер карты: {found_card} за {time_taken:.2f} секунд")
            QMessageBox.information(self, "Успех", 
                                  f"Найден номер карты: {found_card}\n"
                                  f"Время поиска: {time_taken:.2f} секунд")
        else:
            self.status_bar.setText("Номер карты не найден")
            QMessageBox.warning(self, "Ошибка", "Номер карты не найден.")

    def check_card(self):
        card_number = self.card_input.text()
        if len(card_number) != 16 or not card_number.isdigit():
            self.status_bar.setText("Ошибка: номер карты должен состоять из 16 цифр")
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите 16-значный номер карты")
        else:
            is_valid = luhn_algorithm(card_number)
            result = "действителен" if is_valid else "недействителен"
            self.status_bar.setText(f"Номер карты {card_number} {result} по алгоритму Луна")
            QMessageBox.information(self, "Результат", 
                                  f"Номер карты {card_number[:4]} **** **** {card_number[-4:]}\n"
                                  f"Результат проверки: {result}")

    def measure_time(self):
        self.status_bar.setText("Измерение производительности...")
        QApplication.processEvents()

        from visualizer import measure_time_and_plot, visualize_results
        found_card, processes_list, times = measure_time_and_plot()
        visualize_results(processes_list, times)

        if found_card:
            self.status_bar.setText(f"Найден номер карты: {found_card}")
            QMessageBox.information(self, "Успех", 
                                  f"Найден номер карты: {found_card}\n"
                                  f"Результаты производительности сохранены на графике")
        else:
            self.status_bar.setText("Номер карты не найден во время измерения производительности")
            QMessageBox.warning(self, "Ошибка", "Номер карты не найден.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 245, 245))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(233, 231, 227))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(76, 175, 80))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    window = CollisionFinderApp()
    window.show()
    sys.exit(app.exec_()) 