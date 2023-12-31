import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def gradient_descent_1D(f, x_range, x_init, learning_rate=0.1, max_iterations=100):
    x = x_init
    xall = [x]
    yall = [f(x)]

    x_val = np.linspace(x_range[0], x_range[1], 1000)
    y_val = f(x_val)

    fig, ax = plt.subplots()
    ax.plot(x_val, y_val)
    line, = ax.plot([], [], 'ro-')

    def animate(frames):
        nonlocal x
        df_dx = (f(x + 0.00001) - f(x)) / 0.00001  # Numerical differentiation
        x = x - learning_rate * df_dx
        xall.append(x)
        yall.append(f(x))
        line.set_data(xall, yall)
        return line,

    ani = FuncAnimation(fig, animate, frames=max_iterations, interval=100, blit=True)
    ani.save('animation.gif', writer=PillowWriter(fps=2))
    print("Minimum value:", yall[-1])
    print("Minimum point :", xall[-1])


def f1(x):
    return x ** 2 + 3 * x + 8


x_init1 = 5
learning_rate1 = 0.1
max_iterations1 = 20
x_range1 = (-5, 5)


def f2(x):
    return np.cos(x)**4 - np.sin(x)**3 - 4*np.sin(x)**2 + np.cos(x) + 1


x_init2 = 3
learning_rate2 = 0.1
max_iterations2 = 25
x_range2 = (0, 2*np.pi)

#gradient_descent_1D(f2, x_range2, x_init2, learning_rate2, max_iterations1)

gradient_descent_1D(f1, x_range1, x_init1, learning_rate1, max_iterations1)