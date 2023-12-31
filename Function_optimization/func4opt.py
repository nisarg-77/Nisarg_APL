import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def f5(x):
    return np.cos(x)**4 - np.sin(x)**3 - 4*np.sin(x)**2 + np.cos(x) + 1


def df5_dx(x):
    return np.sin(x)*(np.cos(x)**3)*(-4) - (np.sin(x)**2)*(3*np.cos(x)) - (8*np.sin(x)*np.cos(x)) - np.sin(x)


x_val = np.linspace(0, np.pi, 1000)

y_val = f5(x_val)

# plt.plot(x_val, y_val)
# plt.show()

min_value = 10
min_x = 0.2
fig, ax = plt.subplots()
ax.plot(x_val, y_val)
xall, yall = [], []
lnall, = ax.plot([], [], 'ro')
lngood, = ax.plot([], [], 'go', markersize=10)
lr = 0.05


def onestepderiv(frame):
    global min_value, min_x, lr
    x = min_x - df5_dx(min_x) * lr
    min_x = x
    min_value = f5(x)
    lngood.set_data(x, min_value)
    xall.append(x)
    yall.append(min_value)
    lnall.set_data(xall, yall)
    print(min_x, min_value)


ani = FuncAnimation(fig, onestepderiv, frames=range(20), interval=500, repeat=False)
plt.show()
print(min_value, min_x)