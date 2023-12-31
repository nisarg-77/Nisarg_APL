import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation,PillowWriter


def gradient_descent_2D(f, df_dx, df_dy, x_range, y_range, x_init, y_init, learning_rate_x, learning_rate_y, max_iterations):
    x = x_init
    y = y_init
    xall, yall, zall = [x], [y], [f(x, y)]

    x_val = np.linspace(x_range[0], x_range[1], 100)
    y_val = np.linspace(y_range[0], y_range[1], 100)

    X, Y = np.meshgrid(x_val, y_val)
    Z = f(X, Y)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z)

    fig.suptitle("Gradient Descent Optimization")

    min_value = f(x, y)
    min_x, min_y = x, y

    lnall, = ax.plot([], [], [], 'ro', markersize=10)
    lngood, = ax.plot([x], [y], [min_value], 'go', markersize=10)

    def onestepderiv(frame):
        nonlocal x, y, min_value, min_x, min_y
        x = x - learning_rate_x * df_dx(x, y)
        y = y - learning_rate_y * df_dy(x, y)
        current_value = f(x, y)
        xall.append(x)
        yall.append(y)
        zall.append(current_value)
        lnall.set_data(xall, yall)
        lnall.set_3d_properties(zall)
        min_value = current_value
        min_x, min_y = x, y
        lngood.set_data([x], [y])
        lngood.set_3d_properties([min_value])

    ani = FuncAnimation(fig, onestepderiv, frames=range(max_iterations), interval=100, repeat=False)
    ani.save('animation.gif', writer=PillowWriter(fps=10))
    print("Minimum value:", min_value)
    print("Minimum point (x, y):", (min_x, min_y))


def f1(x, y):
    return x ** 4 - 16 * x ** 3 + 96 * x ** 2 - 256 * x + y ** 2 - 4 * y + 262


def df_dx1(x, y):
    return 4 * x ** 3 - 48 * x ** 2 + 192 * x - 256


def df_dy1(x, y):
    return 2 * y - 4


x_range = (-10, 10)
y_range = (-10, 10)
x_init = -5
y_init = 0
learning_rate_x = 0.001
learning_rate_y = 0.1
max_iterations = 200


def f2(x, y):
    return np.exp(-(x - y)**2) * np.sin(y)


def df2_dx(x, y):
    return -2 * np.exp(-(x - y)**2) * np.sin(y) * (x - y)


def df2_dy(x, y):
    return np.exp(-(x - y)**2) * np.cos(y) + 2 * np.exp(-(x - y)**2) * np.sin(y)*(x - y)


x_range2 = (-np.pi, np.pi)
y_range2 = (-np.pi, np.pi)
x_init2 = 1
y_init2 = 1
learning_rate_x2 = 0.1
learning_rate_y2 = 0.1
max_iterations2 = 200


#gradient_descent_2D(f1, df_dx1, df_dy1, x_range, y_range, x_init, y_init, learning_rate_x, learning_rate_y, max_iterations)

gradient_descent_2D(f2, df2_dx, df2_dy, x_range2, y_range2, x_init2, y_init2, learning_rate_x2, learning_rate_y2, max_iterations2)

