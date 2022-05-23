import numpy as np
import matplotlib.pyplot as plt
import time
from DP.py import (inp, readf)

def init(popsize,n): 
    population=[]
    for i in range(popsize):
        pop=''
        for j in range(n):
            pop=pop+str(np.random.randint(0,2))
        population.append(pop)    
    return population

def decode(x,n,w,c,W):
    s=[]
    g=0
    f=0
    for i in range(n):
        if (x[i] == '1'):
            if g+w[i] <= W:
                g = g+w[i]
                f = f+c[i]
                s.append(i)
            else:
                break
    return f,s

def fitnessfun(population,n,w,c,W):
    value=[]
    ss=[]
    for i in range(len(population)):
        [f,s]= decode(population[i],n,w,c,W)
        value.append(f)
        ss.append(s)
    return value,ss

def roulettewheel(population,value,pop_num):
    fitness_sum=[]
    value_sum=sum(value)
    fitness=[i/value_sum for i in value]
    for i in range(len(population)):
        if i==0:
            fitness_sum.append(fitness[i])
        else:
            fitness_sum.append(fitness_sum[i-1]+fitness[i])
    population_new=[]
    for j in range(pop_num):
        r=np.random.uniform(0,1)
        for i in range(len(fitness_sum)):
            if i==0:
                if r>=0 and r<=fitness_sum[i]:
                    population_new.append(population[i])
            else:
                if r>=fitness_sum[i-1] and r<=fitness_sum[i]:
                    population_new.append(population[i])
    return population_new

def crossover(population_new,pc,ncross):
    a=int(len(population_new)/2)
    parents_one=population_new[:a]
    parents_two=population_new[a:]
    np.random.shuffle(parents_one)
    np.random.shuffle(parents_two)
    offspring=[]
    for i in range(a):
        r=np.random.uniform(0,1)
        if r<=pc:
            point1=np.random.randint(0,(len(parents_one[i])-1))
            point2=np.random.randint(point1,len(parents_one[i]))
            off_one=parents_one[i][:point1]+parents_two[i][point1:point2]+
...         parents_one[i][point2:]
            off_two=parents_two[i][:point1]+parents_one[i][point1:point2]+
...         parents_two[i][point2:]
            ncross = ncross+1
        else:
            off_one=parents_one[i]
            off_two=parents_two[i]
        offspring.append(off_one)
        offspring.append(off_two)
    return offspring

def mutation(offspring,pm,nmut):
    for i in range(len(offspring)):
        r=np.random.uniform(0,1)
        if r<=pm:
            point=np.random.randint(0,len(offspring[i]))
            if point==0:
                if offspring[i][point]=='1':
                    offspring[i]='0'+offspring[i][1:]
                else:
                    offspring[i]='1'+offspring[i][1:]
            else:
                if offspring[i][point]=='1':
                    offspring[i]=offspring[i][:(point-1)]+'0'+offspring[i][point:]
                else:
                    offspring[i]=offspring[i][:(point-1)]+'1'+offspring[i][point:]
            nmut = nmut+1
    return offspring

YY = []
XX = []

f, name = inp()

Y, X, C, n, m, c1, c2 = readf(f)

gen=500 #Количество итераций
pc=0.25 #Кросс вероятность
pm=0.02 #Вероятность мутации
popsize= len(X)*2 #Численность популяции
n = len(X) #Длина хромосомы
start_time = time.perf_counter()

 # Инициализация популяции (кодирование)

population=init(popsize,n)
 # декодирование

value,s = fitnessfun(population,n,X,Y,C)

 # Начало кроссовера
ncross=0
 # Начало мутации
nmut=0
 # Сохранение оптимальной стоимости из каждого поколения и соответствующей ему хромосомы
t=[]
best_ind=[]
last=[]# Сохранение ценности фитнесс-функции из последнего поколения
realvalue=[]# Сохранение декодированного значения из последнего поколения


for i in range(gen):
    offspring_c=crossover(population,pc,ncross)
    offspring_m=mutation(offspring_c,pm,nmut)
    mixpopulation=population+offspring_m
    value,s = fitnessfun(mixpopulation,n,X,Y,C)
    population=roulettewheel(mixpopulation,value,popsize)
    result=[]
    if i==gen-1:
        value1,s1 = fitnessfun(population,n,X,Y,C)
        realvalue=s1
        result=value1
        last=value1
    else:
        value1,s1 = fitnessfun(population,n,X,Y,C)
        result=value1
    maxre=max(result)
    h=result.index(max(result))
# Добавление оптимального решения из каждого поколения в конечную популяцию
    t.append(maxre)
    best_ind.append(population[h])

# Вывод результата
best_value=max(t)
hh=t.index(max(t))
f2,s2 = decode(best_ind[hh],n,X,Y,C)

finish_time = time.perf_counter()

print('Оптимальная комбинация:')
print(s2)
print('Оптимальное решение:')
print(f2)
result_time = finish_time-start_time
print("\nЗатраченное время:", round(result_time, 3))
# plt.plot(t)
