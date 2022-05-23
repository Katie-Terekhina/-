import numpy as np
import time
from DP.py import (inp, readf)

YY = []
XX = []

f, name = inp()
Y, X, C, n, m, c1, c2 = readf(f)

if n != m:
    print ('Ошибка в данных: несовпадение размерностей весов и цен')
else:
    print( "Данные (цена, вес):" )
    for k in range( n ):
        print( k + 1, "\b: ", Y[k], " ", X[k] )
    print("\nКоличество предметов:", n )
    print( "\nВместимость рюкзака:", C )
    
HRF = []
HRF_ns = []


for i in range(n):
    k = Y[i]/X[i]
    HRF.append(k)
    HRF_ns.append(k)

A = Y
numb = list(range(n))
A = np.vstack([A, X])
A = np.vstack([A, HRF])
numb = list(map(lambda num: num + 1, numb))
A = np.vstack([A, numb])
A_tr = A.transpose()
A_tr_sort = sorted(A_tr, key=lambda a_entry: a_entry[2], reverse = True) 
AA_tr_sort = np.asarray(A_tr_sort)
# A_sort = AA_tr_sort.transpose
# print(AA_tr_sort)

print( "\nРешение R1:" ) 
C_ost = C
tot_price = 0
tot_weight = 0
index = []
for i in range(n):
    if AA_tr_sort[i][1] <= C_ost:
        C_ost = C_ost - AA_tr_sort[i][1]
        tot_price += AA_tr_sort[i][0]
        tot_weight += AA_tr_sort[i][1]
        index.append(int(AA_tr_sort[i][3]))
        print (int(AA_tr_sort[i][3]),": ", int(AA_tr_sort[i][0]), " ", 
...     int(AA_tr_sort[i][1]) )
    else: continue
        
f = open(name, "a")      
tot_weight = int(tot_weight)
tot_price = round(int(tot_price) + c1*(int(CC) - int(tot_weight)))
print("\nОбщая стоимость:", tot_price, "\b, общий вес:", tot_weight)
f.write("\nРешение методом R1:")
f.write("\nНомера выбранных предметов: ")
index_str = ', '.join(str(x) for x in index)
f.write(index_str)
tot = str(tot_weight)
val = str(tot_price)
f.write("\nОбщая стоимость: " + val + "\b, общий вес: " + tot)
finish_time = time.perf_counter()
result_time = finish_time-start_time
print("\nЗатраченное время:", round(result_time,3))
res_time = str(round(result_time, 3))
f.write("\nЗатраченное время:" + res_time)
f.close()
