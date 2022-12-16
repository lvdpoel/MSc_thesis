# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 10:07:20 2022

@author: l_vdp
"""
import pandas as pd
#%%

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
# #%%
# twr  = pd.read_csv(folder_data+'tower_shuffled_3009.csv',
#                index_col=0)
# air = pd.read_csv(folder_data+'airborne_shuffled_2410.csv',
#                  index_col=0)
mer = pd.read_csv(folder_data+'merged_shuffled_2111.csv',
                index_col=0)
air = pd.read_csv(folder_data+'airborne_shuffled_2410.csv',
                 index_col=0)
#%%
df=air
Grs = df[df.Grs > 0.8]

#%%
peat_cls = ['hV', 'W','pV', 'kV', 'hVz', 'V',  'Vz', 'aVz', 'kVz', 'overigV']
nopeat_cls = ['zandG', 'zeeK', 'rivK', 'gedA', 'leem']
#%%
Grs['peat'] = Grs[peat_cls].sum(axis=1)
Grs['nopeat'] = Grs[nopeat_cls].sum(axis=1)

#%%
peat = Grs[Grs.peat>0.99]
#%%
peat.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/merged_peat99.csv")
#%%

soil_classes = ['hV', 'W', 'pV', 'kV', 'hVz', 'V',
       'Vz', 'aVz', 'kVz', 'overigV', 'zandG', 'zeeK', 'rivK', 'gedA', 'leem']

peat_cls = ['hV', 'W','pV', 'kV', 'hVz', 'V',  'Vz', 'aVz', 'kVz', 'overigV']
nopeat_cls = ['zandG', 'zeeK', 'rivK', 'gedA', 'leem']
zand_cls = ['zandG']
klei_cls = ['zeeK', 'rivK']
loam_gedA = ['gedA', 'leem']

#%%
df = air
df['peat'] = df[peat_cls].sum(axis=1)
df['no_peat'] = df[nopeat_cls].sum(axis=1)
df['sand'] = df['zandG']
df['clay'] = df[klei_cls].sum(axis=1)
df['rest'] = df[loam_gedA].sum(axis=1)
#%%
soil_grps = ['peat', 'sand', 'clay', 'rest']
#%%
df['soilgroup'] = df[soil_grps].idxmax(axis=1)
df['soilclass'] = df[soil_classes].idxmax(axis=1)


#%%
#%%
LGN_classes = ['Grs', 'SuC', 'SpC', 'Ghs', 'dFr', 'cFr', 'Wat',
       'Bld', 'bSl', 'Hth', 'FnB', 'Shr']

df['LGNclass']= df[LGN_classes].idxmax(axis=1)
#%%
df.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/airborne_shuffled_2511.csv")




    






























