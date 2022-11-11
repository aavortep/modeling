import random
from itertools import islice
import sys  # sys нужен для передачи argv в QApplication
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
import tables


COUNT = 100
STEP = 1


class Tables(QtWidgets.QMainWindow, tables.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.table_1.setRowCount(10)
        self.table_1.setColumnCount(1)
        #self.generate()

        self.table_2.setRowCount(COUNT // STEP)
        self.table_2.setColumnCount(3)
        self.rand_alg(0, 10, 0)
        self.rand_alg(10, 100, 1)
        self.rand_alg(100, 1000, 2)

        self.table_3.setRowCount(COUNT // STEP)
        self.table_3.setColumnCount(3)
        self.rand_table()

        self.push_comp.clicked.connect(self.check_randomness)

    def generate(self):
        for i in range(10):
            rand = random.randint(0, 9)
            self.table_1.setItem(i, 0, QTableWidgetItem(str(rand)))

    def rand_alg(self, low, high, col):  # Лемер
        m = 2. ** 31
        a = 1664525
        c = 1013904223
        current = 10
        seq = []
        for i in range(COUNT):
            current = (a * current + c) % m
            result = int(low + current % (high - low))
            seq.append(result)
        for i in range(0, COUNT, STEP):
            self.table_2.setItem(i // STEP, col, QTableWidgetItem(str(seq[i])))

    def rand_table(self):
        numbers = set()
        with open('digits.txt') as file:
            line_num = 0
            lines = islice(file, line_num, None)
            for l in lines:
                numbers.update(set(l.split(" ")[1:-1]))
                line_num += 1
                if len(numbers) >= 3 * COUNT + 1:
                    break
            numbers.remove("")
            numbers = list(numbers)[:3 * COUNT]
        one_digit = [int(i) % 10 for i in numbers[:COUNT]]
        two_digits = [int(i) % 90 + 10 for i in numbers[COUNT:COUNT * 2]]
        three_digits = [int(i) % 900 + 100 for i in numbers[COUNT * 2:3 * COUNT]]
        for i in range(0, len(one_digit), STEP):
            self.table_3.setItem(i // STEP, 0, QTableWidgetItem(str(one_digit[i])))
        for i in range(0, len(two_digits), STEP):
            self.table_3.setItem(i // STEP, 1, QTableWidgetItem(str(two_digits[i])))
        for i in range(0, len(three_digits), STEP):
            self.table_3.setItem(i // STEP, 2, QTableWidgetItem(str(three_digits[i])))

    def _criterion(self, seq):
        bin_seq = ""
        for num in seq:
            bin_seq += bin(num)[2:]
        ones = 0
        for digit in bin_seq:
            if digit == '1':
                ones += 1
        p = ones / len(bin_seq)
        return p

    def _get_sequence(self, table_name, col_num, rows_num):
        seq = []
        table = getattr(self, table_name)
        for i in range(rows_num):
            num = table.item(i, col_num).text()
            seq.append(int(num))
        return seq

    def check_randomness(self):
        seq = self._get_sequence("table_1", 0, 10)
        p = self._criterion(seq)
        self.label_1_1.setText(str(p)[:8])

        seq = self._get_sequence("table_2", 0, COUNT)
        p = self._criterion(seq)
        self.label_2_1.setText(str(p)[:8])
        seq = self._get_sequence("table_2", 1, COUNT)
        p = self._criterion(seq)
        self.label_2_2.setText(str(p)[:8])
        seq = self._get_sequence("table_2", 2, COUNT)
        p = self._criterion(seq)
        self.label_2_3.setText(str(p)[:8])

        seq = self._get_sequence("table_3", 0, COUNT)
        p = self._criterion(seq)
        self.label_3_1.setText(str(p)[:8])
        seq = self._get_sequence("table_3", 1, COUNT)
        p = self._criterion(seq)
        self.label_3_2.setText(str(p)[:8])
        seq = self._get_sequence("table_3", 2, COUNT)
        p = self._criterion(seq)
        self.label_3_3.setText(str(p)[:8])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Tables()
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение
