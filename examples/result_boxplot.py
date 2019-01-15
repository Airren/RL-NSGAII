#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-21 19:15'


import pandas as pd
import numpy as np

from scipy import stats
import matplotlib.pyplot as plt

igd = pd.read_csv('../results/igd.csv',index_col=0,usecols=[0,1,2,3,4])
with open('../results/results.csv','w') as F:
    F.write('ALlgorithm,Mean,VAR,T_value\n')

algorithms = list(igd.columns)

# for i in ['ZDT1','ZDT2','ZDT3','ZDT4','ZDT6']:

for i in set(igd.index):

    with open('../results/results.csv', 'a+') as F:
        F.write(i + ',')
    box_data = igd.ix[i,:]

    # a = box_data.ix[i, 'RL_NSGAII']
    # b = box_data.ix[i, 'NSGAII']
    # c = box_data.ix[i,'RL_NSGAIII']
    # d = box_data.ix[i,'NSGAIII']
    # e = box_data.ix[i, 'SPEA2']
    for j in algorithms:
        with open('../results/results.csv', 'a+') as F:
            F.write(str(np.mean(box_data.ix[i, j]))+','+str(np.var(box_data.ix[i, j]))+'\n')



    # box_data.boxplot()
    igd.ix[i, :].boxplot()
    plt.ylabel("IGD")
    plt.xlabel(i)
    plt.savefig("../results/box_" + i + ".png",dpi=400)
    plt.close()

print("SUCCESS")
