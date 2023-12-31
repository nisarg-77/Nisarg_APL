import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def f1(x):
    return x ** 2 + 3 * x + 8


def df1_dx(x):
    return 2 * x + 3


x_val = np.linspace(-5, 5, 1000)

y_val = f1(x_val)

# plt.plot(x_val, y_val)
# plt.show()

min_value = 1000
min_x = 10
fig, ax = plt.subplots()
ax.plot(x_val,y_val)
xall, yall = [], []
lnall, = ax.plot([], [], 'ro')
lngood, = ax.plot([], [], 'go', markersize=10)
lr = 0.2


def onestepderiv(frame):
    global min_value, min_x, lr
    x = min_x - df1_dx(min_x) * lr
    min_x = x
    min_value = f1(x)
    lngood.set_data(x, min_value)
    xall.append(x)
    yall.append(min_value)
    lnall.set_data(xall, yall)
    # return lngood,


ani = FuncAnimation(fig, onestepderiv, frames=range(20), interval=500, repeat=False)
plt.show()
print(min_value, min_x)