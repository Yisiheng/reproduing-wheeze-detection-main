# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 14:33:44 2021

@author: admin
"""

import gudhi
from gudhi.point_cloud import timedelay
from scipy.io import wavfile
import numpy as np
import pylab as plt 
import statsmodels.tsa.api as sm


#Str="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\wheeze (1).wav"


#open wav file
def Open_file(Str):
    #input:
        #Str: the path of file: string
    #return the mono data of wave file: list of float, shape=(n,1)
    
    sample_rate, wave_data = wavfile.read(Str)
    return wave_data[:,0]

def subsample_Maxmin(data):#shape of data:nx2,2_dim point
    pass

#choose proper delay by caluculate autocorrelation function
def delay_Choice(Sq):
    #input:
        #Sq: the time series: list of float, shape=(n,)
    #return 
        #i: the proper delay: int
    Acf=sm.stattools.acf(Sq, nlags=len(Sq)-1)
    for i in range(len(Acf)):
        if Acf[i]*Acf[i+1]>0:
            continue
        elif abs(Acf[i])>abs(Acf[i+1]):
            return i+1
        else:
            return i

#creat a persistence
def Creat_persistence(Points,max_edge_length=15000.0,max_dimension=2):
    #input: 
        #Points: the point cloud: list of list of float, shape=(n,2);

    #return 
        #diag: the persistence of point cloud by embedding: persistence
    
    #take time embedding
    
    rips_complex=gudhi.RipsComplex(points=Points,max_edge_length=15000.0)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
    
    diag = simplex_tree.persistence(homology_coeff_field=2,min_persistence=50,persistence_dim_max=False)
    
    return diag

#calculate bottleneck distance between 1-dim of persistence and 1-dim of persistence
def Bottleneck_Distance_diag(diag_1,diag_2,e=None):
    #input 
        #diag_1: persistence
        #diag_1: persistence
    #return 
        #bottleneck distance between two persistence
    
    Diag_1=[[],[]]
    Diag_2=[[],[]]
    
    for x in diag_1:
        if x[0]==0:Diag_1[0].append(x[1])
        else:Diag_1[1].append(x[1])
            
    for x in diag_2:
        if x[0]==0:Diag_2[0].append(x[1])
        else:Diag_2[1].append(x[1])
    
    return gudhi.bottleneck_distance(Diag_1[0], Diag_2[0]),gudhi.bottleneck_distance(Diag_1[1], Diag_2[1])



#exhibit the curve of proper delay of all wave file
def Draw_delay():
    #return 
        #Normal_Delay: the delay of normal wave files: list of int, shape=(30,)
        #Wheeze_Delay: the delay of wheeze wave files: list of int, shape=(37,)
    
    Normal=[i+1 for i in range(30)]
    Wheeze=[i+1 for i in range(37)]
    
    Normal_Delay=[]
    Wheeze_Delay=[]
    
    for i in range(len(Normal)):
        Str="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\normal ("+str(Normal[i])+").wav"
        wave_data=Open_file(Str)
        Normal_Delay.append(delay_Choice(wave_data))
        
    plt.figure(num='normal')
    plt.plot(list(range(30)),Normal_Delay)
        
    for i in range(len(Wheeze)):
        Str="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\wheeze ("+str(Wheeze[i])+").wav"
        wave_data=Open_file(Str)
        Wheeze_Delay.append(delay_Choice(wave_data))
        
    plt.figure(num='wheeze')
    plt.plot(list(range(37)),Wheeze_Delay)
    return Normal_Delay,Wheeze_Delay

#sliding window embedding    
def Sliding_Window_Embedding(Sq,Delay=1,Skip=1):
    #input: 
        #Data_Sq: the time series: list of float, shape=(n,1);
        #Delay: delay: int
        #Skip: skip: int
    #return 
        #Points: point cloud of 2-dim
        
    point_Cloud=timedelay.TimeDelayEmbedding(dim=2,delay=Delay,skip=Skip)
    Points=point_Cloud(Sq)
    plt.figure(figsize=(7,7))
    plt.plot(Points[:,0],Points[:,1])
    
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

#subsampling
def SubSampling(Points=None,mode='random',num=50):
    #input
        #Points: crude point cloud: list of list of float, shape=(n,2)
        #mode: how to do subsampling: string, optional: 'random' or 'maxmin' or 'min_squared_dist'
        #num: the number of subsampling or the smallest squared distance between any two points
    #return 
        #subsampling: Subsampled point cloud: list of list of float, shape=(m,2)
    if mode=='random':
        return gudhi.subsampling.pick_n_random_points(Points,nb_points=num)
    elif mode=='maxmin':
        return gudhi.subsampling.choose_n_farthest_points(Points,nb_points=num)
    elif mode=='min_squared_dist':
        return gudhi.subsampling.sparsify_point_set(Points,min_squared_dist=num)
    else:
        print('input mode is error!!!')



"""
#get the delay of every wave file
Normal_Delay=[]
Wheeze_Delay=[]
Normal_Delay,Wheeze_Delay=Draw_delay()

#get the persistence of every wave file
Normal_List=[]
Wheeze_List=[]

for i in range(30):
    Str="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\normal ("+str(i+1)+").wav"
    wave_data=Open_file(Str)
    Points=Sliding_Window_Embedding(wave_data,Delay=Normal_Delay[i],Skip=10)
    Sub_Points=SubSampling(Points,mode='random',num=200)
    Normal_List.append(Creat_persistence(Sub_Points))

for i in range(37):
    Str="C:\\Users\\admin\\Desktop\\Breathing-Sound-Data-master\\Breathing_Sounds\\wheeze ("+str(i+1)+").wav"
    wave_data=Open_file(Str)
    Points=Sliding_Window_Embedding(wave_data,Delay=Wheeze_Delay[i],Skip=10)
    Sub_Points=SubSampling(Points,mode='random',num=200)
    Wheeze_List.append(Creat_persistence(Sub_Points))


#split every persistence into 0-dim and 1-dim
Normal_0_List=[]
Wheeze_0_List=[]
Normal_1_List=[]
Wheeze_1_List=[]

for i in range(30):
    diag_0,diag_1=Split_Persistence(Normal_List[i])
    Normal_0_List.append(diag_0)
    Normal_1_List.append(diag_1)
    
for i in range(37):
    diag_0,diag_1=Split_Persistence(Wheeze_List[i])
    Wheeze_0_List.append(diag_0)
    Wheeze_1_List.append(diag_1)
    
    
"""
    
    
    
    
    
    
    
    
    
    
    
    
    
    


