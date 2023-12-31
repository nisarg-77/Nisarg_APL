import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

xlim3 = [-10, 10]
ylim3 = [-10, 10]


def f3(x, y):
    return x ** 4 - 16 * x ** 3 + 96 * x ** 2 - 256 * x + y ** 2 - 4 * y + 262


def df3_dx(x):
    return 4 * x ** 3 - 48 * x ** 2 + 192 * x - 256


def df3_dy(y):
    return 2 * y - 4


x_val = np.linspace(-10, 10, 100)
y_val = np.linspace(-10, 10, 100)

X, Y = np.meshgrid(x_val, y_val)

z_val = f3(X, Y)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, z_val)
min_value = 100000  # Initialize with a high value
min_x, min_y = 3, 3  # Initialize the minimum point
lngood, = ax.plot([], [], [], 'go', markersize=15)
lnall, = ax.plot([], [], [], 'ro', markersize=10)
lr_x = 0.05
lr_y = 0.1
xall, yall, zall = [], [], []


def onestepderiv(frame):
    global min_value, min_x, min_y, lr_x,lr_y
    x = min_x - df3_dx(min_x) * lr_x
    y = min_y - df3_dy(min_y) * lr_y
    current_value = f3(x, y)
    xall.append(x)
    yall.append(y)
    zall.append(current_value)
    lnall.set_data(xall, yall)
    lnall.set_3d_properties(zall)
    min_value = current_value
    min_x, min_y = x, y
    lngood.set_data(x, y)
    lngood.set_3d_properties(min_value)
    print(x, y)


ani = FuncAnimation(fig, onestepderiv, frames=range(200), interval=100, repeat=False)
plt.show()
print("Minimum value:", min_value)
