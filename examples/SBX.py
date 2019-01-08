#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-25 17:42'

#!/usr/bin/env python
#encoding:UTF-8
import numpy as np
import random

"""
    SBX 模拟二进制交叉

输入：
    population 种群矩阵
    alfa 交叉概率
    numRangeList 决策变量的上限(下限默认为0)
    mu    SBX方式的分布指数, 推荐为1
"""
def cross(population, alfa, numRangeList, mu=1):
    N=population.shape[0]
    V=population.shape[1]
    populationList=range(N)

    for _ in range(N):
        r=random.random()

        if r<alfa:
            p1, p2=random.sample(populationList, 2)
            bq=np.array([0]*V)
            randList=np.random.random(V)
            #根据概率向量判断不同概率函数的选择
            orTF=(randList<=0.5)

            #计算不同决策变量的 不同概率选择 下的 系数
            for j in range(V):
                if orTF[j]==True:
                    bq[j]=(2.0*randList[j])**(1.0/(mu+1))
                else:
                    bq[j]=(1.0/(2.0*(1-randList[j])))**(1.0/(mu+1))

            #取出选定的两个个体
            old_p1=population[p1, ]
            old_p2=population[p2, ]
            #计算交叉后的两个新个体
            new_p1=0.5*((1+bq)*old_p1+(1-bq)*old_p2)
            new_p2=0.5*((1-bq)*old_p1+(1+bq)*old_p2)

            #上下限判断,防止越界
            new_p1=np.max(np.vstack((new_p1, np.array([0]*V))), 0)
            new_p1=np.min(np.vstack((new_p1, numRangeList)), 0)

            new_p2=np.max(np.vstack((new_p2, np.array([0]*V))), 0)
            new_p2=np.min(np.vstack((new_p2, numRangeList)), 0)

            #将交叉后的个体更新回种群
            population[p1, ]=new_p1
            population[p1, ]=new_p2


###以下是测试用例
if __name__=="__main__":
    random.seed(0)
    np.random.seed(0)
    xN=20
    yN=3
    alfa=0.9
    population=np.random.rand(xN*yN).reshape(xN, yN)*1.0

    ###运行函数
    print(population)
    print('-'*50)
    cross(population, alfa, np.array([1]*3))
    print('-'*50)
    print(population)