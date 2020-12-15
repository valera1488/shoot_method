from scipy import integrate
import numpy as np
import math
import matplotlib.pyplot as plt

eps = 0.001

beta = 0.8
alpha = 0.01

a = 0
b = 1

W = 0
H = 0

target_w1 = 0

smoothness = 100


def se_solve(Y, x):
    return [Y[1], (x - 1) / (1 + 1 / (beta * math.sqrt((alpha * Y[1]) ** 2 + 1)))]


def find_section(x, W, H):
    section = [0, 0]
    Y = integrate.odeint(se_solve, [W, H], x)
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

    x = np.linspace(a, b, smoothness)
    y = np.linspace(a, b, smoothness)

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

