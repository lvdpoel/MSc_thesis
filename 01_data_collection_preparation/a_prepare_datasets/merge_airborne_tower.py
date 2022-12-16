# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 21:09:11 2022

@author: l_vdp
"""
import pandas as pd
from sklearn.utils import shuffle
#%%
tower = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/tower_shuffled_3009.csv",
                index_col=0)
tower['source']='tower'
airborne = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/airborne_shuffled_2410.csv",
                 index_col=0)
airborne['source']='airborne'
#%%
merged = pd.concat([tower,airborne])
merged = shuffle(merged)
#%%
merged.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/merged_shuffled_2410.csv")