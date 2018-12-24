#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-18 11:35'

import pandas as pd
import numpy as np
import threading

from scipy.interpolate import spline


from platypus import NSGAII, Problem, Real

import multiprocessing as mp


from platypus import  *
import rl_nsgaii


problems= [ZDT1,ZDT2,ZDT3,ZDT4,ZDT6]


with open('../results/igd.csv','w') as F:
    F.write(",RL_NSGAII,NSGAII\n")



for problem in problems:

    for j in range(5):

        processes = []
        for i in range(20):
            processes.append(mp.Process(target= rl_nsgaii.compare_experiment,args=(problem(),)))
        for i in range(20):
            processes[i].start()
        for i in range(20):
            processes[i].join()

