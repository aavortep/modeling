import random
import numpy
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import sys  # sys нужен для передачи argv в QApplication
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
import inputs
import results

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

    def get_table(self):
        matrix = []
        for i in range(self.states_num):
            row = []
            for j in range(self.states_num):
                row.append(self.matrix.item(i, j).text())
            matrix.append(row)
        return matrix

    def _dp(self, matrix, probabilities):
        res = []
        n = len(matrix)
        for i in range(n):
            summ = 0
            for j in range(n):
                if i == j:
                    sum_i = 0
                    for t in range(n):
                        sum_i += float(matrix[i][t])

                    summ += probabilities[j] * (-1 * sum_i + float(matrix[i][i]))
                else:
                    summ += probabilities[j] * float(matrix[j][i])
            res.append(TIME_DELTA * summ)
        return res

    def get_stab_time(self, matrix, start_probabilities):
        n = len(matrix)
        current_time = 0
        current_probabilities = start_probabilities.copy()
        stabilization_times = [0 for i in range(n)]
        stabilization_p = [0 for i in range(n)]
        prev_probabilities = []
        for i in range(n):
            prev_probabilities.append([])
        x = []
        counter = 0
        prev_dp = self._dp(matrix, current_probabilities)
        while not all(stabilization_times):
            while counter < 100:
                curr_dp = self._dp(matrix, current_probabilities)
                for i in range(n):
                    prev_probabilities[i].append(current_probabilities[i])
                    current_probabilities[i] += curr_dp[i]
                counter += 1
                x.append(current_time)
                current_time += TIME_DELTA
            for i in range(n):
                if not stabilization_times[i] and abs(prev_dp[i] - curr_dp[i]) < EPS and abs(curr_dp[i]) < EPS:
                    stabilization_times[i] = current_time - TIME_DELTA * 30
                    stabilization_p[i] = current_probabilities[i]
            counter = 0
            prev_dp = curr_dp

        counter = 0
        while counter < 100:
            curr_dp = self._dp(matrix, current_probabilities)
            for i in range(n):
                prev_probabilities[i].append(current_probabilities[i])
                current_probabilities[i] += curr_dp[i]
            counter += 1
            x.append(current_time)
            current_time += TIME_DELTA
        fig, ax = plt.subplots()

        for i in range(n):
            ax.plot(x, prev_probabilities[i], label='S' + str(i+1))
            ax.scatter(stabilization_times[i], stabilization_p[i], color='orange', s=40, marker='o')
        ax.legend()
        ax.set_xlabel('Time')
        ax.set_ylabel('Probabilities')
        plt.show()
        return stabilization_times

    def compute(self):
        matrix = self.get_table()

        matrix = numpy.array(matrix)
        n = len(matrix)
        coeff_matrix = numpy.zeros((n, n))

        for state in range(n - 1):
            for col in range(n):
                coeff_matrix[state, state] -= float(matrix[state, col])
            for row in range(n):
                coeff_matrix[state, row] += float(matrix[row, state])

        for state in range(n):
            coeff_matrix[n - 1, state] = 1

        res = [0 for i in range(n)]
        res[n - 1] = 1
        augmentation_matrix = numpy.array(res)

        probs = numpy.linalg.solve(coeff_matrix, augmentation_matrix)

        start_probabilities = [0] * n
        start_probabilities[0] = 1
        stab_time = self.get_stab_time(matrix, start_probabilities)

        self.window = Results(probs, stab_time)
        self.window.show()


class Results(QtWidgets.QMainWindow, results.Ui_MainWindow):
    def __init__(self, probs, stab_time):
        super().__init__()
        self.setupUi(self)

        self.probs_table.setColumnCount(len(probs))
        self.probs_table.setRowCount(1)

        self.stab_table.setColumnCount(len(stab_time))
        self.stab_table.setRowCount(1)

        for i in range(len(probs)):
            prob = str(round(probs[i], 4))
            self.probs_table.setItem(0, i, QTableWidgetItem(prob))

        for i in range(len(stab_time)):
            stab = str(round(stab_time[i], 4))
            self.stab_table.setItem(0, i, QTableWidgetItem(stab))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Inputs()
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение