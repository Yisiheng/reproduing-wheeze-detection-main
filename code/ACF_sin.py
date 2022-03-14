# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 09:37:08 2021

@author: admin
"""

import numpy as np
import pylab as plt 
import statsmodels.tsa.api as sm

def Sin(point_num=10000,delay=1.6,skip=1):
    Point=[]
    for i in range(point_num):
        Point.append((np.sin(i*skip),np.sin(i*skip+delay)))
    return Point

def Sin_(point_num=100,delay=1.6,skip=1):
    Point=[]
    for i in range(point_num):
        Point.append((np.sin(i*skip)+np.sin(2*i*skip),np.sin(i*skip+delay)+np.sin(2*i*skip+2*delay)))
    return Point

def Sin__(point_num=100,delay=1.6,skip=1):
    Point=[]
    for i in range(point_num):
        Point.append((np.sin(i*skip)+100*np.sin(2*i*skip),np.sin(i*skip+delay)+100*np.sin(2*i*skip+2*delay)))
    return Point

"""
Sq_1=[np.sin(i) for i in range(100)]
Acf=sm.stattools.acf(Sq_1, nlags=99)
plt.figure(num='tau')
plt.plot(list(range(100)),Acf)

Point=np.array(Sin(100,3.14/2,1))
plt.figure(figsize=(7,7))
plt.plot(Point[:,0],Point[:,1])


Sq_2=[np.sin(i)+np.sin(2*i) for i in range(100)]
Acf=sm.stattools.acf(Sq_2, nlags=99)
plt.figure(num='tau')
plt.plot(list(range(100)),Acf)

Point=np.array(Sin_(100,3.14/2,1))
plt.figure(figsize=(7,7))
plt.plot(Point[:,0],Point[:,1])

"""

Sq_3=[np.sin(i)+100*np.sin(2*i) for i in range(100)]
Acf=sm.stattools.acf(Sq_3, nlags=99)
plt.figure(num='tau')
plt.plot(list(range(100)),Acf)

Point=np.array(Sin__(1000,1.5,1))
plt.figure(figsize=(7,7))
plt.plot(Point[:,0],Point[:,1])







