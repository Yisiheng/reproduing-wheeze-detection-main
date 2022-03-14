# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:08:55 2021

@author: admin
"""

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
import statsmodels.tsa.api as sm

#open wav file
def Open_file(Str):

    sample_rate, wave_data = wavfile.read(Str)

    return wave_data[:5000,0]


def Creat_persistence(Data=None,Delay=1,Skip=50,file_name=None):
    
    plt.figure()
    plt.plot(list(range(len(Data))),Data)
    
    plt.savefig('C:\\Users\\admin\\Desktop\\picture_PH\\'+file_name+'\\sign.png')
    
    point_Cloud=timedelay.TimeDelayEmbedding(dim=2,delay=Delay,skip=Skip)
    Points=point_Cloud(Data)
    
    plt.figure(figsize=(7,7))
    plt.plot(Points[:,0],Points[:,1])
    
    plt.savefig('C:\\Users\\admin\\Desktop\\picture_PH\\'+file_name+'\\embedding.png')
    
    
    rips_complex=gudhi.RipsComplex(points=Points,max_edge_length=10000.0)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
    
    diag = simplex_tree.persistence(homology_coeff_field=2,min_persistence=100,persistence_dim_max=False)
    
    diag_0=[]
    diag_1=[]
    
    for x in diag:
        if x[0]==0:diag_0.append(x)
        else:diag_1.append(x)
    
    gudhi.plot_persistence_barcode(persistence=diag_0, max_intervals=100, inf_delta=0.1, legend=True)
    plt.savefig('C:\\Users\\admin\\Desktop\\picture_PH\\'+file_name+'\\barcode_0.png')
    gudhi.plot_persistence_diagram(persistence=diag_0, max_intervals=100, inf_delta=0.1, legend=True, greyblock=True)
    plt.savefig('C:\\Users\\admin\\Desktop\\picture_PH\\'+file_name+'\\diagram_0.png')
    
    gudhi.plot_persistence_barcode(persistence=diag_1, max_intervals=100, inf_delta=0.1, legend=True)
    plt.savefig('C:\\Users\\admin\\Desktop\\picture_PH\\'+file_name+'\\barcode_1.png')
    gudhi.plot_persistence_diagram(persistence=diag_1, max_intervals=100, inf_delta=0.1, legend=True, greyblock=True)
    plt.savefig('C:\\Users\\admin\\Desktop\\picture_PH\\'+file_name+'\\diagram_1.png')
    
    return diag

def tau_Choice(Sq):
    
    Acf=sm.stattools.acf(Sq, nlags=len(Sq)-1)
    for i in range(len(Acf)):
        if Acf[i]*Acf[i+1]>0:
            continue
        elif abs(Acf[i])>abs(Acf[i+1]):
            return i+1
        else:
            return i

def Draw_tau():
    
    Normal_List=[]
    Wheeze_List=[]
    
    for i in range(30):
        Str="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\normal ("+str(i+1)+").wav"
        wave_data=Open_file(Str)
        Normal_List.append(tau_Choice(wave_data))
        
    plt.figure(num='normal')
    plt.plot(list(range(30)),Normal_List)
        
    for i in range(37):
        Str="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\wheeze ("+str(i+1)+").wav"
        wave_data=Open_file(Str)
        Wheeze_List.append(tau_Choice(wave_data))
        
    plt.figure(num='wheeze')
    plt.plot(list(range(37)),Wheeze_List)
    return Normal_List,Wheeze_List



Normal_List,Wheeze_List=Draw_tau()

for i in range(30):
    Str='C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\normal ('+str(i+1)+').wav'
    Data=Open_file(Str)
    diag=Creat_persistence(Data,Normal_List[i],10,file_name='normal\\normal('+str(i+1)+')')


for i in range(37):
    Str='C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\wheeze ('+str(i+1)+').wav'
    Data=Open_file(Str)
    diag=Creat_persistence(Data,Wheeze_List[i],10,file_name='wheeze\\wheeze('+str(i+1)+')')











