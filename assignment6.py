import numpy as np
import matplotlib.pyplot as plt
import random

cities_1 = [(0, 1.5), (2.3, 6.1), (4.2, 1.3), (2.1, 4.5)]
cities_2 = [(3.26, 7.01), (6.77, 3.82), (9.69, 9.97), (7.4, 0.33), (4.53, 1.44), (1.91, 3.67), (0.28, 9.05), (6.36, 3.98), (9.13, 8.86), (5.99, 4.36)]


def distance(cities, cityorder):
    totaldistance = 0
    for i in range(len(cities)):
        x_sq = (cities[cityorder[i]][0] - cities[cityorder[i - 1]][0]) ** 2
        y_sq = (cities[cityorder[i]][1] - cities[cityorder[i - 1]][1]) ** 2
        totaldistance += (x_sq + y_sq) ** 0.5

    return totaldistance


def swap_random(seq):
    lent = range(len(seq))
    i1, i2 = random.sample(lent, 2)
    new_seq = seq.copy()
    new_seq[i1], new_seq[i2] = seq[i2], seq[i1]
    return new_seq


def optimize_cities(cities):
    # Initialize variables
    T = 10000
    decayrate = 0.99
    order_initial = list(range(len(cities)))
    np.random.shuffle(order_initial)
    best_order = order_initial
    best_distance = distance(cities, best_order)
    intial_distance = best_distance # initial distance at start to calculate percentage improvement

    fig = plt.figure()

    def update(frame):
        nonlocal order_initial, best_distance, best_order, T
        new_order = swap_random(order_initial)
        dist_new = distance(cities, new_order)
        if dist_new < best_distance:
            best_distance = dist_new
            best_order = new_order
            order_initial = new_order
        else:
            chance = np.random.random_sample()
            if chance < np.exp(-(dist_new - best_distance) / T):
                best_distance = dist_new
                best_order = new_order
                order_initial = new_order

        T *= decayrate

    for i in range(100000):
        update(i)

    new_cities_x = [cities[i][0] for i in order_initial]
    new_cities_x.append(new_cities_x[0])
    new_cities_y = [cities[i][1] for i in order_initial]
    new_cities_y.append(new_cities_y[0])
    plt.plot(new_cities_x, new_cities_y, marker='o', linestyle='-', markersize=10)
    improvement = ((intial_distance - best_distance)/intial_distance)*100
    print("Optimum order : ", best_order)
    print("Distance trvaelled : ", best_distance)
    print("Percentage improvement : ", improvement)
    plt.show()


def extract_cities(filename):
    data_list = []

    try:
        with open(filename, 'r') as file:
            next(file) # skips first line
            for line in file:
                values = [float(x) for x in line.split()]
                data_list.append(tuple(values))
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

    return data_list


cities_3 = extract_cities("tsp40.txt")

optimize_cities(cities_3)
# optimize_cities(cities_2)
#optimize_cities(cities_1)
