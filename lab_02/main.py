import random
import numpy
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import sys  # sys нужен для передачи argv в QApplication
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
import inputs
TIME_DELTA = 1e-3
EPS = 1e-5


class Inputs(QtWidgets.QMainWindow, inputs.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.apply.clicked.connect(self.build_table)
        self.add.clicked.connect(self.add_lmbda)
        self.generate.clicked.connect(self.gen_table)
        self.start.clicked.connect(self.compute)

    def build_table(self):
        self.states_num = int(self.statesNum.text())
        self.matrix.setColumnCount(self.states_num)
        self.matrix.setRowCount(self.states_num)
        for i in range(self.states_num):
            self.matrix.setItem(i, i, QTableWidgetItem("0"))

    def add_lmbda(self):
        from_state = int(self.fromState.text())
        to_state = int(self.toState.text())
        if from_state == to_state:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Начальное и конечное состояния должны быть разными")
            dlg.exec()
        else:
            lmbda = self.lmbda.text()
            self.matrix.setItem(from_state - 1, to_state - 1, QTableWidgetItem(lmbda))

    def gen_table(self):
        for i in range(self.states_num):
            for j in range(self.states_num):
                if i != j:
                    item = str(round(random.random(), 4))
                    self.matrix.setItem(i, j, QTableWidgetItem(item))

    def compute(self):
        #


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Inputs()
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение
