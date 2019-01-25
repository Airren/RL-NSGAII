#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2019-01-14 09:27'

from glob import glob
import pandas as pd
import matplotlib.pyplot as plt




algorithms = ["NSGAII","RL_NSGAII","NSGAIII","RL_NSGAIII"]
problems = ["ZDT_1","ZDT_2","ZDT_3","ZDT_4","ZDT_6",]

numbers  = [50,100,150,200]

for number in numbers:

    for problem in problems:

        igd = {}
        for algorithm in algorithms:
            files = glob(r"//Users/airren/Desktop/results/"+problem+"/"+algorithm+"/*.csv")
            igd[algorithm] = []

            for file in files:
                data = pd.read_csv(file, index_col=0, header=-1,)

                igd[algorithm].append(data[1][number])

        igd = pd.DataFrame(igd)

        igd.boxplot()
        plt.ylabel("IGD")
        plt.xlabel(problems)
        plt.savefig("../results/box_" + problem+str(number) + ".png",dpi=400)
        plt.close()
        # plt.show()

print("SUCCESS")








