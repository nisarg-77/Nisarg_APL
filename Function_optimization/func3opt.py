import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


xlim4 = [-np.pi, np.pi]


def f4(x, y):
    return np.exp(-(x - y)**2) * np.sin(y)


def df4_dx(x, y):
    return -2 * np.exp(-(x - y)**2) * np.sin(y) * (x - y)


def df4_dy(x, y):
    return np.exp(-(x - y)**2) * np.cos(y) + 2 * np.exp(-(x - y)**2) * np.sin(y)*(x - y)


x_val = np.linspace(-np.pi, np.pi, 100)
y_val = np.linspace(-np.pi, np.pi, 100)

X,Y = np.meshgrid(x_val,y_val)

z_val = f4(X, Y)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, z_val)
min_value = 100000  # Initialize with a high value
min_x, min_y = -np.pi,-np.pi  # Initialize the minimum point
lngood, = ax.plot([], [], [], 'go', markersize=20)
lnall, = ax.plot([], [], [], 'ro', markersize=10)
lr = 0.3
xall, yall, zall = [], [], []


def onestepderiv(frame):
    global min_value, min_x, min_y, lr
    x = min_x - df4_dx(min_x, min_y) * lr
    y = min_y - df4_dy(min_x, min_y) * lr
    current_value = f4(x, y)
    if current_value < min_value:
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
    else:
        pass


ani = FuncAnimation(fig, onestepderiv, frames=range(200), interval=100, repeat=False)
plt.show()
print("Minimum value:", min_value)