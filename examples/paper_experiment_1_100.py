#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-18 11:35'



import multiprocessing as mp

from platypus import  *

# from examples import paper_experiment
import paper_experiment

problems= [ZDT1,ZDT2,ZDT3,ZDT4,ZDT6]
with open('../results/igd.csv', 'a+') as F:
    F.write(',RL_NSGAII,NSGAII,RL_NSGAIII,NSGAIII,SPEA2,\n')

for problem in problems:

    for j in range(6):

        processes = []
        for i in range(20):
            processes.append(mp.Process(target= paper_experiment.compare_experiment,args=(problem(),)))
        for i in range(20):
            processes[i].start()
        for i in range(20):
            processes[i].join()
