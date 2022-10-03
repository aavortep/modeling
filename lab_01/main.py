import matplotlib.pyplot as plt
from math import exp, sqrt, pi
from sympy import exp as sym_exp, symbols, integrate, oo
import numpy
import sys


start = -100
stop = 101
n_start = -20
n_stop = 20


def uniform_density(a, b, x):
    if a <= x <= b:
        return 1 / (b - a)
    return 0


def normal_density(sigma, m, x):
    return 1 / (sigma * sqrt(2 * pi)) * exp(-(x - m) ** 2 / (2 * sigma ** 2))


def uniform_distribution(a, b, x):
    if x < a:
        return 0
    elif x > b:
        return 1
    else:
        return (x - a) / (b - a)


def integral(sigma, m, x):
    t = symbols('t')
    expr = sym_exp(-(t - m) ** 2 / (2 * sigma ** 2))
    return integrate(expr, (t, -oo, x)).evalf()


def normal_distribution(sigma, m, x):
    return 1 / (sqrt(2 * pi) * sigma) * integral(sigma, m, x)


def normal(sigma, m):
    distribution_x = [i for i in range(n_start, n_stop + 1)]
    distribution_y = [normal_distribution(sigma, m, x) for x in distribution_x]
    prepare_show_normal(distribution_x, distribution_y, "График функции нормального распределения",
                        "x", "F(x)", sigma, m)
    plt.show()

    density_x = [i for i in range(n_start, n_stop + 1)]
    density_y = [normal_density(sigma, m, x) for x in density_x]
    prepare_show_normal(density_x, density_y, "График функции плотности нормального распределения",
                        "x", "f(x)", sigma, m)
    plt.show()


def uniform(a, b):
    distribution_x = [i for i in range(start, stop + 1)]
    distribution_y = [uniform_distribution(a, b, x) for x in distribution_x]
    prepare_show_uniform(distribution_x, distribution_y, "График функции равномерного распределения",
                         "x", "F(x)", a, b)
    plt.show()

    density_x = numpy.linspace(start, stop + 1, num=500)
    density_y = [uniform_density(a, b, x) for x in density_x]
    prepare_show_uniform(density_x, density_y, "График функции плотности равномерного распределения",
                         "x", "f(x)", a, b)
    plt.show()


def prepare_show_normal(x_value, y_value, title, x_label, y_label, sigma, m):
    plt.plot(x_value, y_value)
    plt.grid(True)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)

    label = "σ = " + str(sigma) + " m = " + str(m)
    plt.text(x_value[-2], min(y_value), label, fontsize=10)


def prepare_show_uniform(x_value, y_value, title, x_label, y_label, a, b):
    plt.plot(x_value, y_value)
    plt.grid(True)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)

    label = "a = " + str(a) + " b = " + str(b)
    plt.text(x_value[-2], min(y_value), label, fontsize=10)


if __name__ == '__main__':
    a, b = map(int, input("Введите (через пробел) значения параметров a и b "
                          "для равномерного распределения: ").split())

    if a >= b:
        print("Параметр a должен быть меньше параметра b")
        sys.exit(0)
    uniform(a, b)

    m, sigma = map(int, input("Введите (через пробел) значения параметров m и σ "
                              "для нормального распределения: ").split())
    if sigma <= 0:
        print("σ должна быть больше 0")
        sys.exit(0)
    else:
        normal(sigma, m)
