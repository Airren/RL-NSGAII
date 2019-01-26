#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-18 11:35'

import pandas as pd
import numpy as np
import threading
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
from platypus import  *



def compare_experiment(problem):

    times = 205

    pup = 100
    ref_set = problem.get_ref_set()

    # algorithms = [RL_NSGAII,NSGAII,SPEA2,(NSGAIII,100)]

    algorithms = [
        RL_NSGAII,
        NSGAII,
        (RL_NSGAIII, {"divisions_outer": 4}),
        (NSGAIII, {"divisions_outer": 4}),
        # (CMAES, {"epsilons": [0.05]}),
        # GDE3,
        # IBEA,
        # (MOEAD, {"weight_generator": normal_boundary_weights, "divisions_outer": 50}),
        # (OMOPSO, {"epsilons": [0.05]}),
        # SMPSO,
        # RL_SPEA2,
        # SPEA2,
        # (EpsMOEA, {"epsilons": [0.05]})
    ]

    # run the experiment using Python 3's concurrent futures for parallel evaluation
    with ProcessPoolEvaluator() as evaluator:
        results = experiment(algorithms, problem, seeds=1, nfe=times*pup, evaluator=evaluator)

    # display the results


    # Corlor Table https://www.cnblogs.com/darkknightzh/p/6117528.html
    # red lawgreen  aqua darkred  darkorange deepskyblue
    # 'hotpink': '#FF69B4',
    # 'slateblue':            '#6A5ACD',
    colors = ['#FF0000','#7CFC00','#00FFFF','#8B0000','#FF8C00','#00BFFF','#FF69B4','#6A5ACD',]
    # fig.tight_layout()  # 调整整体空白
    plt.figure(figsize=(30,5))
    plt.subplots_adjust(wspace=0.3, hspace=0)  # 调整子图间距

    for i, algorithm in enumerate(six.iterkeys(results)):
        result = results[algorithm][type(problem).__name__][0]

        plt.subplot(1, len(results) + 1, i + 1, projection='3d')
        plt.title(algorithm)
        plt.xlabel("$f_1(x)$")
        plt.ylabel("$f_2(x)$")
        plt.scatter([k.objectives[0] for k in ref_set],
                    [k.objectives[1] for k in ref_set],
                    [k.objectives[2] for k in ref_set], c='b', marker='.', )

        plt.scatter([k.objectives[0] for k in result],
                    [k.objectives[1] for k in result],
                    [k.objectives[2] for k in result], c=colors[i], marker='x')

    #
    plt.subplot(1, len(results)+1, len(results)+1)
    plt.title(type(problem).__name__)
    plt.xlabel("$Generations$")
    plt.ylabel("$IGD$")

    for i, algorithm in enumerate(six.iterkeys(results)):
        result = results[algorithm][type(problem).__name__][1]
        plt.plot(list(range(len(result))), result, c=colors[i], marker="",label=algorithm,linewidth = '1',)
        pd.Series(result).to_csv("../results/"+str(type(problem).__name__)+"_"+time.strftime("%m-%d_%H-%M-%S", time.gmtime())+'_'+str(algorithm)+".csv")
    plt.legend(loc=1)

    plt.savefig("../results/"+str(type(problem).__name__)+'_'+time.strftime("%m-%d_%H-%M-%S", time.gmtime())+".png",dpi=300)
    # plt.show()
    plt.close()


    with open('../results/igd.csv', 'a+') as F:
        F.write(str(type(problem).__name__) + ',')
        for i, algorithm in enumerate(six.iterkeys(results)):
            result = results[algorithm][type(problem).__name__][1]
            F.write(str(result[-1])+ ',')
        F.write('\n')

    with open('../results/hv.csv', 'a+') as F:
        F.write(str(type(problem).__name__) + ',')
        for i, algorithm in enumerate(six.iterkeys(results)):
            result = results[algorithm][type(problem).__name__][2]
            F.write(str(result[-1])+ ',')
        F.write('\n')





if __name__ == "__main__":
    # for i in [WFG4(2),WFG5(2),WFG6(2),WFG7(2),WFG8(2),WFG9(2),]:
    #     compare_experiment(i)
    compare_experiment(DTLZ2(6))



























