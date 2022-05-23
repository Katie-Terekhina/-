import numpy as np
import time
from DP.py import (inp, readf)

def total_valu_size(packing, values, sizes, max_size):
  # total value and size of a specified packing
    v = 0.0  # общая ценность набора
    s = 0.0  # общий вес набора
    n = len(packing)
    for i in range(n):
        if packing[i] == 1:
            v += values[i]
            s += sizes[i]
    if s >= max_size:  # too big to fit in knapsack
        v = 0.0
    return (v, s)

def adjacent(packing, rnd):
    n = len(packing)
    result = np.copy(packing)
    i = rnd.randint(n)
    if result[i] == 0:
        result[i] = 1
    elif result[i] == 1:
        result[i] = 0
    return result

def solve(n_items, rnd, values, sizes, max_size, max_iter, start_temperature, alpha):
    curr_temperature = start_temperature
    curr_packing = np.ones(n_items, dtype=np.int64)
    print("Initial guess: ")
    print(curr_packing)
    (curr_valu, curr_size) = total_valu_size(curr_packing, values, sizes, max_size)
    iteration = 0
    interval = (int)(max_iter / 10)
    while iteration <= max_iter:
        adj_packing = adjacent(curr_packing, rnd)
        (adj_v, _) = total_valu_size(adj_packing, values, sizes, max_size)
        if adj_v >= curr_valu:  # принимаем переход к соседнему решению, если оно лучше
            curr_packing = adj_packing; curr_valu = adj_v
        else:          # случай, когда соседнее решение хуже
            accept_p = np.exp( (adj_v - curr_valu ) / curr_temperature ) 
            p = rnd.random()
            if p <= accept_p:  # принятие ухудшающего решения
                curr_packing = adj_packing; curr_valu = adj_v 
          # else don't accept
        if iteration % interval == 0:
            print("iter = %6d : curr value = %7.0f : curr temp = %10.2f " %
...         (iteration, curr_valu, curr_temperature))

        if curr_temperature <= stop:
            curr_temperature = stop
        else:
            curr_temperature *= alpha
      # curr_temperature = start_temperature * \
      # pct_iters_left * 0.0050
        iteration += 1

    return curr_packing       

YY = []
XX = []

f, name = inp()

Y, X, C, n, m, c1, c2 = readf(f)


values = Y
sizes = X
max_size = C

print("\nЦены: ")
print(values)
print("\nВеса: ")
print(sizes)
print("\nЁмкость ранца = %d " % max_size)

rnd = np.random.RandomState(5)
max_iter = 1000
start_temperature = 10000.0
alpha = 0.99
stop = 0.00001

print("\nПараметры: ")
print("Максимальное кол-во итераций = %d " % max_iter)
print("Начальная температура = %0.1f " % start_temperature)
print("alpha = %0.2f " % alpha)

print("\nНачальное решение: ")
packing = solve(n, rnd, values, sizes, max_size, max_iter, start_temperature, alpha)
print("Последнее решение: ")

print("\nЛучшее найденное решение: ")
print(packing)
(v,s) = total_valu_size(packing, values, sizes, max_size)
print("\nОбщая стоимость = %0.1f " % v)
print("\nОбщий вес = %0.1f " % s)
