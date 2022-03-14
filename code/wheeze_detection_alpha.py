# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 08:46:06 2021

@author: admin
"""

import gudhi
from gudhi.point_cloud import timedelay
from scipy.io import wavfile
import numpy as np
import pylab as plt 


#open wav file
def Open_file(Str):

    sample_rate, wave_data = wavfile.read(Str)

    return wave_data[:5000,0]


def Creat_persistence(Data,Delay=1,Skip=50):
    
    plt.figure()
    plt.plot(list(range(len(Data))),Data)
    
    
    point_Cloud=timedelay.TimeDelayEmbedding(dim=2,delay=Delay,skip=Skip)
    Points=point_Cloud(Data)
    
    plt.figure(figsize=(7,7))
    plt.plot(Points[:,0],Points[:,1])
    

    
    rips_complex=gudhi.RipsComplex(points=Points,max_edge_length=10000.0)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
    
    diag = simplex_tree.persistence(homology_coeff_field=2,min_persistence=100,persistence_dim_max=False)
    
    diag_0=[]
    diag_1=[]
    
    for x in diag:
        if x[0]==0:diag_0.append(x)
        else:diag_1.append(x)
    
    gudhi.plot_persistence_barcode(persistence=diag_0, max_intervals=100, inf_delta=0.1, legend=True)
    gudhi.plot_persistence_diagram(persistence=diag_0, max_intervals=100, inf_delta=0.1, legend=True, greyblock=True)
    
    gudhi.plot_persistence_barcode(persistence=diag_1, max_intervals=100, inf_delta=0.1, legend=True)
    gudhi.plot_persistence_diagram(persistence=diag_1, max_intervals=100, inf_delta=0.1, legend=True, greyblock=True)
    
    return diag


Str_normal="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\normal (3).wav"
Str_wheeze="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\wheeze (3).wav"

Data_normal=Open_file(Str_normal)
Data_wheeze=Open_file(Str_wheeze)

diag_normal=Creat_persistence(Data_normal,47,10)

diag_wheeze=Creat_persistence(Data_wheeze,40,10)


"""
"bottleneck distance"
diag_normal_1=[]
diag_wheeze_1=[]

for x in diag_normal:
    if x[0]==0:continue
    else:diag_normal_1.append(x[1])
    
for x in diag_wheeze:
    if x[0]==0:continue
    else:diag_wheeze_1.append(x[1])


print("---------------------------------------------------")
print("normal (3).wav:delay=47; wheeze (3).wav:delay=40;")
print("bottlenect distance between 1-dims of normal and wheeze:",gudhi.bottleneck_distance(diag_normal_1, diag_wheeze_1))
print("---------------------------------------------------")
"""








