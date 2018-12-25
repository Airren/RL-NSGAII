#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018-12-25 17:42'

import matplotlib.pyplot as plt
import numpy as np
import  pandas as pd
x= np.arange(1,20,1)
plt.plot(x,x**2,label='Fast')#label为标签
plt.plot(x,x*2,label='Mormal')#l
plt.legend(loc=0,ncol=2)#图例及位置： 1右上角，2 左上角 loc函数可不写 0为最优 ncol为标签有几列
#此处若是不写plt.legend，则不会显示标签
plt.show()
