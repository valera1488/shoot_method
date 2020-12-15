from scipy import integrate
import numpy as np
import math
import matplotlib.pyplot as plt

# точность
eps = 0.001

# константы
beta = 0.8
alpha = 0.01

# границы
a = 0
b = 1

# начальные условия задачи Коши
W = 0  # W(0) = 0
H = 0  # H(0) = 0

# целевое значение W(1)
target_w1 = 0

# параметр гладкости кривой на графике (больше - лучше)
smoothness = 100

"""
для решения задач Коши я использую модуль scipy.integrate
работает он так: в функцию odeint передается 3 параметра
1 - функция которая задает систему ОДУ первого порядка
2 - начальные условия задачи Коши
3 - список значений независимой переменной (x) в которых нужно найти решение. 
Первым значением последовательности должено быть число, от которого берутся
начальные условия.
"""


def se_solve(Y, x):  # параметры - список значений [W, H] и 'x'
    """
    Разобьем исходное уравнение второго порядка, на систему ОДУ первого порядка,
    выполнив подставновки:
    y = W                        Г W' = H                                              y(1) = W(1) = 1
            => получаем систему <                           , с соответствующими граничными условиями
    H = W'                       L H' = x - 1 / (...)                                  y'(0) = W'(0) = H(0) = 0
    """
    # возвращаем W' = H = второй элемент списка
    #            H' = функция от W - первый элемент списка
    return [Y[1], (x - 1) / (1 + 1 / (beta * math.sqrt((alpha * Y[1]) ** 2 + 1)))]


def find_section(x, W, H):
    section = [0, 0]
    Y = integrate.odeint(se_solve, [W, H], x)  # находим отрезок, на котором располагается решение задачи
    if Y[-1][0] > target_w1:
        section[1] = H
        while Y[-1][0] > target_w1:
            H -= 0.5
            Y = integrate.odeint(se_solve, [W, H], x)
        section[0] = H
    else:
        section[0] = H
        while Y[-1][0] < target_w1:
            H += 0.5
            Y = integrate.odeint(se_solve, [W, H], x)
        section[1] = H
    return section


if __name__ == '__main__':
    # массивы для решения задачи
    # генерируем иксы от 'b' до 'a' в которых будем получать решение (стреляем в обратном направлении,
    #                                                                   т.к. задано граничное условие y для правого края)
    x = np.linspace(a, b, smoothness)
    y = np.linspace(a, b, smoothness)
    # интегрируем систему уравнений

    section = find_section(x, W, H)
    H = (section[1] + section[0]) / 2
    Y = integrate.odeint(se_solve, [W, H], x)

    while abs(Y[-1][0] - target_w1) > eps:
        if Y[-1][0] > target_w1:
            section[1] = H
        else:
            section[0] = H
        H = (section[1] + section[0]) / 2
        Y = integrate.odeint(se_solve, [W, H], x)

    for i in range(0, len(Y)):
        y[i] = Y[i][0]
    plt.plot(x, y, c='blue', label="y(x)")

    for i in range(0, len(Y)):
        y[i] = Y[i][1]
    plt.plot(x, y, c='green', label="y'(x)")
    plt.grid()
    plt.legend()
    plt.show()

