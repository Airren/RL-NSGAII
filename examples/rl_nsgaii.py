#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-18 11:35'

import pandas as pd
import numpy as np
import threading

from scipy.interpolate import spline


from platypus import NSGAII, Problem, Real


from platypus import  *


def compare_experiment(problem):
    times = 2

    # problem = Schaffer()
    # problem = ZDT4()
    algorithm = RL_NSGAII(problem)
    a = algorithm.population_size
    algorithm.run(a*times)


    algorithm.RL.q_table.to_csv("./q_table_zdt2.csv")
    ref_set = problem.get_ref_set()

    # Calculate the performance metrics.
    hyp = Hypervolume(reference_set = ref_set)
    print("Hypervolume:", hyp.calculate(algorithm.result))

    gd = GenerationalDistance(reference_set = ref_set)
    print("GD:", gd.calculate(algorithm.result))

    igd = InvertedGenerationalDistance(reference_set = ref_set)
    print("IGD:", igd.calculate(algorithm.result))

    aei = EpsilonIndicator(reference_set = ref_set)
    print("Eps-Indicator:", aei.calculate(algorithm.result))

    spacing = Spacing()
    print("Spacing:", spacing.calculate(algorithm.result))



    algorithm2 = NSGAII(problem)
    a = algorithm2.population_size
    algorithm2.run(a*times)
    ref_set = problem.get_ref_set()





    # plot the results using matplotlib
    import matplotlib.pyplot as plt
    plt.subplot(1,2,1)
    plt.xlabel("$f_1(x)$")
    plt.ylabel("$f_2(x)$")
    plt.title(type(problem).__name__)
    plt.scatter([s.objectives[0] for s in ref_set],
                [s.objectives[1] for s in ref_set],c = 'b',marker='.')
    plt.scatter([s.objectives[0] for s in algorithm.result],
                [s.objectives[1] for s in algorithm.result],c = 'r',marker='.')



    plt.scatter([s.objectives[0] for s in algorithm2.result],
                [s.objectives[1] for s in algorithm2.result],c = '#FFD700',marker='x')
    plt.subplot(1,2,2)
    plt.plot(list(range(len(algorithm.igd))),algorithm.igd,c = 'r', marker="")
    # plt.plot(list(range(len(algorithm.hyp))),algorithm.hyp,c = 'r', marker="")
    # plt.plot(list(range(len(algorithm.gd))),algorithm.gd,c = 'r', marker="")
    # plt.plot(list(range(len(algorithm.aei))),algorithm.aei,c = 'r', marker="")
    # plt.plot(list(range(len(algorithm.spacing))),algorithm.spacing,c = 'r', marker="")

    plt.plot(list(range(len(algorithm2.igd))),algorithm2.igd,c = '#FFD700', marker="")
    # plt.plot(list(range(len(algorithm2.gd))),algorithm2.gd,c = '#FFD700', marker="")
    # plt.plot(list(range(len(algorithm2.hyp))),algorithm2.hyp,c = '#FFD700', marker="")


    print("RL_NSGA: ",algorithm.igd[-1])

    print("NSGA: ",algorithm2.igd[-1])



    with open('../results/igd.csv', 'a+') as F:
        F.write(str(type(problem).__name__)+','+str(algorithm.igd[-1])+','+str(algorithm2.igd[-1])+'\n')

    # xnew = np.linspace(0,len(algorithm.igd),1200)
    # y = spline(list(range(len(algorithm.igd))),algorithm.igd,xnew)
    # plt.plot(xnew,y)

    # plt.xlim([0, 1.1])
    # plt.ylim([0, 1.1])
    plt.xlabel("$evolution times$")
    plt.ylabel("$IGD$")
    plt.savefig("../results/"+str(type(problem).__name__)+'_'+time.strftime("%m-%d_%H-%M-%S", time.gmtime())+".png")
    # plt.show()
    plt.close()



if __name__ == "__main__":
    compare_experiment(ZDT3())



























