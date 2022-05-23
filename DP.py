import numpy as np
import time

def knapsack( C, weight, cost, n ):
    K = [ [0 for x in range(C + 1)] for x in range(n + 1) ] 
    for i in range( n + 1):
        for w in range( C + 1 ):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif weight[i - 1] <= w:
                K[i][w] = max(K[i - 1][w], cost[i - 1] + K[i - 1][w - weight[i-1]]) 
            else:
                K[i][w] = K[i - 1][w] 
    return K 


YY = []
XX = []

def inp():
    print ("Для использования готового файла введите 1\nДля создания случайного файла введите 2")
    aa = int(input())
    if aa == 1 : 
        print ("Введите имя файла")
        name = input()
        ff = open(name, "r")
    
    elif aa == 2 :
        print ('Введите имя нового файла')
        name = input()
        print ('Введите вместимость рюкзака')
        cap = int(input())
        cap_min = 0.1*cap
        cap_max = 0.3*cap
        print ('Введите количество предметов')
        am = int(input())
        u = 0.1*am
        v = 0.5*am
        PP = []
        PP = np.random.randint(u, v, am)
        prices = ', '.join(str(x) for x in PP)
        WW = []
        WW = np.random.randint(cap_min, cap_max, am)
        weights = ', '.join(str(x) for x in WW)
        ff = open(name, "w+")
        cap = str(cap)
        ff.write(prices + '\n' + weights + '\n' + cap)
        ff.close()
        ff = open(name, "r")
        
    else :
        print ('Введена неправильная цифра')
        break
        
    return(ff, name)

# чтение из файла: информация о предметах по строкам (цена Y, вес X) 
# последняя строка: вместимость рюкзака (C)

def readf(ff):
    y = ff.readline()
    for num in y.strip().split(','):
        YY.append(num)
    x = ff.readline()
    for num in x.strip().split(','):
        XX.append(num)
    CC = ff.readline()
    
    # преобразование из str в int
    Y = [int(x) for x in YY]
    X = [int(x) for x in XX]
    C = int(CC)
    
    # n - количество предметов
    n = len(Y)
    m = len(X)
    
    c1 = 0.5*max(X)/(1.5*C)
    c2 = 1.5*max(X)/(0.5*C)
    
    return(Y, X, C, n, m, c1, c2)

Y, X, C, n, m, c1, c2 = readf(f)

start_time = time.perf_counter()
if n != m:
    print ('Ошибка в данных: несовпадение размерностей весов и цен')
else:
    print( "Данные (цена, вес):" )
    for k in range( n ):
        print( k + 1, "\b: ", Y[k], " ", X[k] ) 
    print("\nКоличество предметов:", n )
    print( "\nВместимость рюкзака:", C )   
 
    K = knapsack( C, X, Y, n )
    index = []
    f = open(name, "a")
    print( "\nОптимальное решение:" ) 
    w, i, tot_weight = C, n, 0 
    res = K[n][C]
    f.write("\nНомера выбранных предметов: ")
    while i > 0 and res > 0:
        if res != K[i - 1][w]:
            print( i,": ", Y[i - 1], " ", X[i - 1] )
            index.append(i)
            tot_weight += X[i - 1]
            res -= Y[i - 1] 
            w -= X[i - 1]
        i -= 1  
        
    tot = str(tot_weight)
    val = str(K[n][C])
    tot_price = round(K[n][C] + c1*(int(CC) - int(tot_weight)))
    print("\nОбщая стоимость:", tot_price, "\b, общий вес:", tot_weight)
    index_str = ', '.join(str(x) for x in index)
    f.write(index_str)
    f.write("\nОбщая стоимость: " + val + "\b, общий вес: " + tot)
    finish_time = time.perf_counter()
    result_time = finish_time-start_time
    print("\nЗатраченное время:", round(result_time, 3))
    res_time = str(round(result_time, 3))
    f.write("\nЗатраченное время:" + res_time)
    f.close()
