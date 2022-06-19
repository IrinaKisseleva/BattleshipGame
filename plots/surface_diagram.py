import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


def show_diagram(X, Y, Z):
    figure, axes = plt.subplots(subplot_kw={'projection': '3d'})

    X, Y = np.meshgrid(X, Y)
    Z = np.array(Z)

    # Создание поверхности
    surf = axes.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)

    # Настройка цветовой панели, которая соотносит значения с определенными цветами
    figure.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


def show_ships_diagram(ships):
    # масштаб
    scale = 2
    scaled_len = scale * 11
    # заполнение x и y от 0 до масштаба
    X = range(scaled_len)
    Y = range(scaled_len)
    # заполение двумерного массива z 1 - x 2 - y
    Z = [[0] * scaled_len for _ in range(scaled_len)]
    for ship in ships:
        # нахождение кординат кораблей
        for i in range(len(ship)):
            x = (ship[i][0]) * scale
            y = (ship[i][1]) * scale
            Z[x][y] = len(ship)

    show_diagram(X, Y, Z)
