# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 17:30:36 2022

@author: l_vdp

Script to prepare the tower data:
- rename columns to match airborne data
- calculate vapour pressure deficit
- drop rows without PAR or CO2 value
- throw out highest and lowest 0.5%
- shuffle data


"""
#%% some imports

import pandas as pd
from sklearn.utils import shuffle


#%% get tower data (already overlaid with spatial info)
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"

twr  = pd.read_csv(folder_data+'tower_shuffled_3009.csv',
               index_col=0)

#%% rename columns to match airborne data

# key = old name
# value = new name
dict = {'FCO2': 'CO2flx', 'rH':'RH', 
        'APAR': 'PAR_abs',  'Temp': 'Tsfc', 
        'Date':'datetime'}

twr.rename(columns=dict,  inplace=True)

#%% calculate vapour rpessure deficit

#https://betterorganix.com/blog/what-is-how-to-calculate-vapour-pressure-deficit/
twr['VPsat'] = (610.78 * 10 ** ((7.5 * twr['Tsfc'])/(twr['Tsfc'] + 237.3 ))) / 1000
twr['VPair'] = twr['VPsat'] * (twr['RH'] / 100)
twr['VPD'] = twr['VPsat'] - twr['VPair']

#%% drop rows where CO2 or PAR is NaN

twr = twr.dropna(axis=0, subset=['CO2flx', 'PAR_abs'])

#%% throw out highest 0.5% and lowest 0.5%

lw = lw[(lw['CO2flx'] > lw.CO2flx.quantile(0.005)) & (lw['CO2flx'] < lw.CO2flx.quantile(0.995))]
zv = zv[(zv['CO2flx'] > zv.CO2flx.quantile(0.005)) & (zv['CO2flx'] < zv.CO2flx.quantile(0.995))]

# merge in one dataframe
df = pd.concat([lw, zv])
print(df.isna().sum())
len(df)
df.index = range(len(df))
#%%
twr_shf = shuffle(twr)


#%%

twr_shf.to_csv(r'C:/Users\l_vdp\Documents\MSc_Thesis\data\preprocessing\towers\DataLangeweideZegveld\lw_zv_99_maps.csv')

