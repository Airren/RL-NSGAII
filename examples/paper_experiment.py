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

    times = 200
    ref_set = problem.get_ref_set()

    # algorithms = [RL_NSGAII,NSGAII,SPEA2,(NSGAIII,100)]

    algorithms = [
        RL_NSGAII,
        NSGAII,
        (RL_NSGAIII, {"divisions_outer": 100}),
        (NSGAIII, {"divisions_outer": 100}),
        # (CMAES, {"epsilons": [0.05]}),
        # GDE3,
        # IBEA,
        # (MOEAD, {"weight_generator": normal_boundary_weights, "divisions_outer": 100}),
        # (OMOPSO, {"epsilons": [0.05]}),
        # SMPSO,
        SPEA2,
        # (EpsMOEA, {"epsilons": [0.05]})
    ]

    # run the experiment using Python 3's concurrent futures for parallel evaluation
    with ProcessPoolEvaluator() as evaluator:
        results = experiment(algorithms, problem, seeds=1, nfe=20000, evaluator=evaluator)

    # display the results


    # Corlor Table https://www.cnblogs.com/darkknightzh/p/6117528.html
    # red lawgreen darkorange darkred aqua deepskyblue
    # 'hotpink': '#FF69B4',
    # 'slateblue':            '#6A5ACD',
    colors = ['#FF0000','#7CFC00','#FF8C00','#8B0000','#00FFFF','#00BFFF','#FF69B4','#6A5ACD',]
    # fig.tight_layout()  # 调整整体空白
    plt.figure(figsize=(20,5))
    plt.subplots_adjust(wspace=0.3, hspace=0)  # 调整子图间距

    for i, algorithm in enumerate(six.iterkeys(results)):
        result = results[algorithm][type(problem).__name__][0]

        plt.subplot(1, len(results) + 1, i + 1)
        plt.title(algorithm)
        plt.xlabel("$f_1(x)$")
        plt.ylabel("$f_2(x)$")
        plt.scatter([s.objectives[0] for s in ref_set],
                    [s.objectives[1] for s in ref_set], c='b', marker='.')

        plt.scatter([s.objectives[0] for s in result],
                    [s.objectives[1] for s in result], c=colors[i], marker='.')



    plt.subplot(1, len(results)+1, len(results)+1)
    plt.title(type(problem).__name__)
    plt.xlabel("$evolution times$")
    plt.ylabel("$IGD$")

    for i, algorithm in enumerate(six.iterkeys(results)):
        result = results[algorithm][type(problem).__name__][1]
        plt.plot(list(range(len(result))), result, c=colors[i], marker="",label=algorithm)
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





if __name__ == "__main__":
    compare_experiment(ZDT2())



























