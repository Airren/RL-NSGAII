# Program Name: NSGA-II.py
# Description: This is a python implementation of Prof. Kalyanmoy Deb's popular NSGA-II algorithm
# Author: Haris Ali Khan
# Supervisor: Prof. Manoj Kumar Tiwari

#Importing required modules
import math
import random
import matplotlib.pyplot as plt

import pandas as pd

#First function to optimize
def function1(x):
    value = x**2
    return value

#Second function to optimize
def function2(x):
    value = (x-2)**2
    return value

#Function to find index of list
def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1

#Function to sort by values
def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1:
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = math.inf
    return sorted_list

#Function to carry out NSGA-II's fast non dominated sort
def fast_non_dominated_sort(values1, values2):
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0,len(values1)):
        S[p]=[]
        n[p]=0
        for q in range(0, len(values1)):
            if (values1[p] <= values1[q] and values2[p] <= values2[q]) :
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] <= values1[p] and values2[q] <= values2[p]) :
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)

    del front[len(front)-1]
    return front

#Function to calculate crowding distance
def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted1[k+1]] - values2[sorted1[k-1]])/(max(values1)-min(values1))
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
    return distance

#Function to carry out the crossover
def crossover(a,b):
    r=random.random()
    if r>0.5:
        return mutation((a+b)/2)
    else:
        return mutation((a-b)/2)

#Function to carry out the mutation operator
def mutation(solution):
    mutation_prob = random.random()
    if mutation_prob <1:
        solution = min_x+(max_x-min_x)*random.random()
    return solution



'''
种群大小
评估次数（进化代数）

变异率
交叉率
'''
POPULATION_SIZE = 10
MAX_GENERATION = 1000

MUTATION_RATE = 0.06
CROSSOVER_RATE = 0.9

'''
决策空间（约束条件）
'''
min_x = -50
max_x = 55

'''
初始化种群
'''
solution = [min_x + (max_x - min_x) * random.random() for i in range(0, POPULATION_SIZE)]
gen_no = 0

'''
生成第1个子代
'''

while(gen_no<MAX_GENERATION):

    '''
    快速非支配排序
    '''
    function1_values = [function1(solution[i])for i in range(0,POPULATION_SIZE)]
    function2_values = [function2(solution[i])for i in range(0,POPULATION_SIZE)]
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:],function2_values[:])
    print("The best front for Generation number ",gen_no, " is")
    for valuez in non_dominated_sorted_solution[0]:
        print(round(solution[valuez],3),end=" ")
    print("\n")

    '''
       拥挤度计算
    '''

    crowding_distance_values=[]
    for i in range(0,len(non_dominated_sorted_solution)):
        crowding_distance_values.append(crowding_distance(function1_values[:],function2_values[:],non_dominated_sorted_solution[i][:]))
    '''
       生成并合并父代和子代
    '''
    solution2 = solution[:]
    #Generating offsprings
    while(len(solution2)!=2*POPULATION_SIZE):
        a1 = random.randint(0,POPULATION_SIZE-1)
        b1 = random.randint(0,POPULATION_SIZE-1)
        solution2.append(crossover(solution[a1],solution[b1]))

    '''
    生成新parents
    '''
    function1_values2 = [function1(solution2[i])for i in range(0,2*POPULATION_SIZE)]
    function2_values2 = [function2(solution2[i])for i in range(0,2*POPULATION_SIZE)]
    non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:],function2_values2[:])
    crowding_distance_values2=[]
    for i in range(0,len(non_dominated_sorted_solution2)):
        crowding_distance_values2.append(crowding_distance(function1_values2[:],function2_values2[:],non_dominated_sorted_solution2[i][:]))
    new_solution= []
    for i in range(0,len(non_dominated_sorted_solution2)):
        non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i] ) for j in range(0,len(non_dominated_sorted_solution2[i]))]
        front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
        front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
        front.reverse()
        for value in front:
            new_solution.append(value)
            if(len(new_solution)==POPULATION_SIZE):
                break
        if (len(new_solution) == POPULATION_SIZE):
            break
    solution = [solution2[i] for i in new_solution]
    gen_no = gen_no + 1

#Lets plot the final front now
function1 = [i  for i in function1_values]
function2 = [j  for j in function2_values]

c = {
    'function1':function1,
    'function2':function2
}

results = pd.DataFrame(c)

results.to_csv("./result1.csv")

plt.xlim(0, 4)
plt.ylim(0, 4)
plt.xlabel('Function 1', fontsize=15,)
plt.ylabel('NSGA', fontsize=15)
plt.scatter(function1, function2,c='r',marker='.')
plt.show()