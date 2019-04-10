#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-21 19:15'


import pandas as pd
import numpy as np

# from scipy import stats
import matplotlib.pyplot as plt

# igd = pd.read_csv('../results/hv.csv',index_col=0,usecols=[0,1,2,3,4])
# with open('../results/results_hv.csv','w') as F:
#     F.write(',RL_NSGAII,NSGAII,RL_NSGAIII,NSGAIII\n')
#
# algorithms = list(igd.columns)
#
# # for i in ['ZDT1','ZDT2','ZDT3','ZDT4','ZDT6']:
#
# for i in set(igd.index):
#
#     with open('../results/results_hv.csv', 'a+') as F:
#         F.write(i)
#     box_data = igd.ix[i,:]
#
#     # a = box_data.ix[i, 'RL_NSGAII']
#     # b = box_data.ix[i, 'NSGAII']
#     # c = box_data.ix[i,'RL_NSGAIII']
#     # d = box_data.ix[i,'NSGAIII']
#     # e = box_data.ix[i, 'SPEA2']
#     for j in algorithms:
#         with open('../results/results_hv.csv', 'a+') as F:
#             F.write(','+str(np.mean(box_data.ix[i, j]))+',\n,'+str(np.var(box_data.ix[i, j]))+'\n')
#
#
#
#     # box_data.boxplot()
#     igd.ix[i, :].boxplot()
#     plt.ylabel("HV")
#     plt.xlabel(i)
#     plt.savefig("../results/hv_box_" + i + ".png",dpi=400)
#     plt.close()

igd = pd.read_csv('../results/igd.csv',index_col=0,usecols=[1,2])
with open('../results/results_igd.csv','w') as F:
    F.write(',RL_NSGAII,NSGAII,RL_NSGAIII,NSGAIII\n')

algorithms = list(igd.columns)[:2]

# for i in ['ZDT1','ZDT2','ZDT3','ZDT4','ZDT6']:



for i in set(igd.index):

    with open('../results/results_igd.csv', 'a+') as F:
        F.write(i)
    box_data = igd.loc[i,:]

    # a = box_data.ix[i, 'RL_NSGAII']
    # b = box_data.ix[i, 'NSGAII']
    # c = box_data.ix[i,'RL_NSGAIII']
    # d = box_data.ix[i,'NSGAIII']
    # e = box_data.ix[i, 'SPEA2']
    for j in algorithms:
        with open('../results/results_igd.csv', 'a+') as F:
            F.write(','+str(np.mean(box_data.loc[i, j]))+',\n,'+str(np.var(box_data.loc[i, j]))+'\n')

    # plt.figure(figsize=(6, 4))

    tables = igd.loc[i, :].boxplot(return_type='dict',showmeans=True,grid=True)

    # for a, b in zip(df['num'], df['resultRate']):
    #     plt.text(a, b + 0.001, '%.4f' % b, ha='center', va='bottom', fontsize=9)
    #
    for median,mean in zip(tables['medians'],tables["means"]):
        plt.text(median._x[1]+0.02,median._y[0],
                 'median: %.4f\n mean: %.4f' %(median._y[0],mean._y[0]),ha='left', va='bottom',
                 fontsize=8,color='teal')
    plt.grid(axis="y", ls=":", lw=1, color="gray", alpha=0.4)

    # for median in tables['medians']:
    #     plt.text(median._x[1] + 0.02, median._y[1], 'mean: %.4f' % median._y[1], ha='left', va='bottom', fontsize=9)

    #
    #
    #     # 箱体边框颜色
    #     # box.set(width=1600)
    #     # 箱体内部填充颜色
    #     box.set(animated=True)
    plt.ylabel("IGD")
    plt.xlabel(i)
    plt.savefig("../results/igd_box_" + i + ".png",dpi=500)
    plt.close()

print("SUCCESS")
