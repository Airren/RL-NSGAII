#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-18 11:35'

import pandas as pd
import numpy as np
import threading


import matplotlib.pyplot as plt
from platypus import  *



def compare_experiment(problem):

    times = 100
    ref_set = problem.get_ref_set()

    algorithms = [RL_NSGAII,NSGAII,(RL_NSGAIII,100)]


    # Corlor Table https://www.cnblogs.com/darkknightzh/p/6117528.html
    # red lawgreen darkorange darkred aqua deepskyblue

    colors = ['#FF0000','#7CFC00','#FF8C00','#8B0000','#00FFFF','#00BFFF',]
    markers = ['.','.','.']

    results = {}

    for algorithm in algorithms:
        if isinstance(algorithm, tuple):
            pass
            algorithm = algorithm[0](problem,algorithm[1])
            a = algorithm.population_size
            algorithm.run(a * times)
        else:
            algorithm = algorithm(problem)
            a = algorithm.population_size
            algorithm.run(a * times)
        i = type(algorithm).__name__
        results[i] = []
        results[i].append(algorithm.result)
        results[i].append(algorithm.igd)

    # fig.tight_layout()  # 调整整体空白
    plt.figure(figsize=(20,5))
    plt.subplots_adjust(wspace=0.3, hspace=0)  # 调整子图间距



    for i,j in enumerate(results):
        plt.subplot(1, len(results)+1, i+1)
        plt.title(j)
        plt.xlabel("$f_1(x)$")
        plt.ylabel("$f_2(x)$")
        plt.scatter([s.objectives[0] for s in ref_set],
                    [s.objectives[1] for s in ref_set], c='b', marker='.',s=0.5)



        plt.scatter([s.objectives[0] for s in results[j][0]],
                    [s.objectives[1] for s in results[j][0]], c=colors[i], marker='x')


    plt.subplot(1, len(results)+1, len(results)+1)
    plt.title(type(problem).__name__)
    plt.xlabel("$evolution times$")
    plt.ylabel("$IGD$")

    for i, j in enumerate(results):
        plt.plot(list(range(len(results[j][1]))), results[j][1], c=colors[i], marker="",label=j)
        print(results[j][1][-1])



    plt.legend(loc=1)

    # plt.legend(plots,['RL_NSGAII','NSGAII','SPEA2','NSGAIII'])

    plt.savefig("../results/"+str(type(problem).__name__)+'_'+time.strftime("%m-%d_%H-%M-%S", time.gmtime())+".png",dpi=300)
    # plt.show()
    plt.close()


    with open('../results/igd.csv', 'a+') as F:
        F.write(str(type(problem).__name__) + ',')
        for i in results:
            F.write(str(results[i][1][-1])+ ',')
        F.write('\n')

if __name__ == "__main__":
    compare_experiment(DTLZ4(6))



























