# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 12:46:29 2021

@author: admin
"""

#wheeze (11), wheeze (17), wheeze (19), wheeze (23), wheeze (28)


import gudhi
from gudhi.point_cloud import timedelay
from scipy.io import wavfile
import numpy as np
import pylab as plt 
import statsmodels.tsa.api as sm

def tau_Choice(Sq):
    
    Acf=sm.stattools.acf(Sq, nlags=len(Sq)-1)
    for i in range(len(Acf)):
        if Acf[i]*Acf[i+1]>0:
            continue
        elif abs(Acf[i])>abs(Acf[i+1]):
            return i+1
        else:
            return i

def Open_file(Str):

    sample_rate, wave_data = wavfile.read(Str)
    time=list(range(len(wave_data)))
    #plt.figure()
    plt.subplot(2,1,1)
    plt.plot(time,wave_data[:,0])
    plt.subplot(2,1,2)
    plt.plot(time,wave_data[:,1],c="r")
    plt.xlabel("time")
    plt.show()
    
    return wave_data[:,0]

def Sliding_Window_Embedding(Sq,Delay=1,Skip=1):
    point_Cloud=timedelay.TimeDelayEmbedding(dim=2,delay=Delay,skip=Skip)
    Points=point_Cloud(Sq)
    plt.figure(figsize=(7,7))
    plt.scatter(Points[:,0], Points[:,1],s=0.3)
    
    return Points

#split every persistence into 0-dim and 1-dim
def Split_Persistence(diag):
    #input 
        #diag: persistence
    #return 
        #diag_0: persistence of 0_dim
        #diag_1: persistence of 1_dim
    
    diag_0=[]
    diag_1=[]
    
    for x in diag:
        if x[0]==0:diag_0.append(x)
        else:diag_1.append(x)
    return diag_0,diag_1

Str="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\wheeze (28).wav"
Sq=Open_file(Str)
Point_Cloud=Sliding_Window_Embedding(Sq,Delay=tau_Choice(Sq))

Sub_Points=gudhi.subsampling.pick_n_random_points(Point_Cloud,nb_points=500)
#Sub_Points=gudhi.subsampling.choose_n_farthest_points(Point_Cloud,nb_points=100)
#Sub_Points=gudhi.subsampling.sparsify_point_set(Point_Cloud,min_squared_dist =1000)

plt.figure()
plt.scatter(np.array(Sub_Points)[:,0], np.array(Sub_Points)[:,1])

rips_complex=gudhi.RipsComplex(points=Sub_Points,max_edge_length=15000.0)
simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
diag = simplex_tree.persistence(homology_coeff_field=2,min_persistence=50,persistence_dim_max=False)
diag_0,diag_1=Split_Persistence(diag)
gudhi.plot_persistence_barcode(persistence=diag_1, max_intervals=100, inf_delta=0.1, legend=True)













