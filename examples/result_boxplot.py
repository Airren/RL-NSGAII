#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-21 19:15'


import pandas as pd
import numpy as np

from scipy import stats
import matplotlib.pyplot as plt

igd = pd.read_csv('../results/igd.csv',index_col=0)
with open('../results/results.csv','w') as F:
    F.write('ALlgorithm,Mean,VAR,T_value\n')

for i in ['ZDT1','ZDT2','ZDT3','ZDT4','ZDT6']:
    if i in set(igd.index):
        box_data = igd.ix[i,:]

        a = box_data.ix[i, 'RL_NSGAII']
        b = box_data.ix[i, 'NSGAII']
        T = stats.ttest_ind(a, b, equal_var=False)
        print("T value: ", T)
        print("Mean value:", np.mean(a), "  ", np.mean(b))
        print("Var value: ", np.var(a), "  ", np.var(b))

        with open('../results/results.csv', 'a+') as F:
            F.write(i+','+str(np.mean(a))+','+str(np.mean(b))+'\n')
            F.write(i + ',' + str(np.var(a)) + ',' + str(np.var(b)) + '\n')
            F.write(i+','+str(T.pvalue)+'\n')

        box_data.boxplot()
        plt.ylabel("IGD")
        plt.xlabel(i)
        plt.savefig("../results/box_" + i + ".png")
        plt.close()

print("SUCCESS")
