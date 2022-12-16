# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 17:30:36 2022

@author: l_vdp

File to prepare the tower data. 
Steps undertaken:
    1. Read data and select useful columns
    2. Throw out rows where F_CO2 = nan
    2. Remove outer 1%
    

"""
#%%
# Some imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import matplotlib.dates as mdates
import numpy as np

#%% Step 1: read data and remove NaNs

#path_lw = "C:\Users\l_vdp\Documents\MSc_Thesis\data\preprocessing\towers\DataLangeweideZegveld\Langeweide.csv"
#path_zv = "C:\Users\l_vdp\Documents\MSc_Thesis\data\preprocessing\towers\DataLangeweideZegveld\Zegveld.csv"
#path_lw = "C:\Users\l_vdp\Documents\MSc_Thesis\data\preprocessing\towers\DataLangeweideZegveld\Langeweide.csv"
#path_zv ="C:\Users\l_vdp\Documents\MSc_Thesis\data\preprocessing\towers\DataLangeweideZegveld\Zegveld.csv"
#%%#%%
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
#%%
twr  = pd.read_csv(folder_data+'tower_shuffled_3009.csv',
               index_col=0)

air = pd.read_csv(folder_data+'airborne_shuffled_1110.csv',
                 index_col=0)

#%%

lw_raw = pd.read_csv(path_lw)
zv_raw = pd.read_csv(path_zv)

#nans are 'nan'
# gebruik met _f: filled met KNMI en NOBV stations

# select columns of interest
lw = lw_raw[['F_CO2', 'datetime', 'hour', 'PAR_f', 'co2_var', 'RH_f', 'VPD_f', 'Tair_f', 'x_90']]
zv = zv_raw[['F_CO2', 'datetime', 'hour', 'PAR_f', 'co2_var', 'RH_f', 'VPD_f', 'Tair_f', 'x_90']]

lw= lw.replace(-9999,pd.NA)
zv = zv.replace(-9999, pd.NA)

#%% rename columns to match airborne data
df=air
# key = old name
# value = new name
dict = {'F_CO2': 'CO2flx', 'RH_f':'RH', 'VPD_f':'VPD',
        'PAR_f': 'PAR',  'Tair_f': 'Tsfc', 'datetime':'Date'}

# rename tower columns to match airborne data

# key = old name
# value = new name
dict = {'FCO2': 'CO2flx', 'rH':'RH', 
        'APAR': 'PAR_abs',  'Temp': 'Tsfc', 
        'BBB': 'BBB_single', 'GWS': 'GWS_single', 'OWD': 'OWD_single', 
        'BBB_area':'BBB', 'GWS_area':'GWS', 'OWD_area': 'OWD'}

dict = {'Date':'datetime'}
# call rename () method
df.rename(columns=dict,  inplace=True)
 
# call rename () method
lw.rename(columns=dict,  inplace=True)
zv.rename(columns=dict,  inplace=True)


#%%
air['NDVI2'] = air['NDVI']/0.9
#%%
#https://betterorganix.com/blog/what-is-how-to-calculate-vapour-pressure-deficit/
data['VPsat'] = (610.78 * 10 ** ((7.5 * data['Tsfc'])/(data['Tsfc'] + 237.3 ))) / 1000
data['VPair'] = data['VPsat'] * (data['RH'] / 100)
data['VPD'] = data['VPsat'] - data['VPair']

#%% Drop NaNs
lw = lw.dropna(axis=0, subset=['F_CO2', 'PAR_f'])
for i in lw.index:
    lw.loc[i, 'datetime'] = datetime.strptime(lw.loc[i,'datetime'], '%Y-%m-%d %H:%M:%S')

zv = zv.dropna(axis=0, subset=['F_CO2', 'PAR_f'])
for i in zv.index:
    zv.loc[i, 'datetime'] = datetime.strptime(zv.loc[i,'datetime'], '%Y-%m-%d %H:%M:%S')
#%%
df = twr # of twr
for i in df.index:
    df.loc[i, 'datetime'] = datetime.strptime(df.loc[i,'datetime'], '%Y-%m-%d %H:%M:%S')
#%%
df=air
for i in df.index:
    df.loc[i, 'datetime'] = datetime.strptime(df.loc[i,'datetime'], ' %Y-%m-%d')

   

#%%
lw.index = range(len(lw))
zv.index = range(len(zv))
#%% use land use class and soil previously calculated
old = pd.read_csv(r"C:\Users\l_vdp\Documents\MSc_Thesis\data\modelling\towers\towerdata_all_99Q_owd_2906_areas_v3.csv", index_col=0)

maps_classes = ['Grs', 'SuC', 'SpC', 'Ghs', 'dFr', 'cFr', 'Wat',
       'Bld', 'bSl', 'Hth', 'FnB', 'Shr','hV', 'W', 'pV', 'kV', 'hVz', 'V',
       'Vz', 'aVz', 'kVz', 'overigV', 'zandG', 'zeeK', 'rivK', 'gedA', 'leem']
 

lwH_info = list(old.loc[old['site'] =='Langeweide_Hoog'][maps_classes].iloc[1])
lwL_info = list(old.loc[old['site'] =='Langeweide_Laag'][maps_classes].iloc[1])
zvH_info = list(old.loc[old['site'] =='Zegveld_Hoog'][maps_classes].iloc[1])
zvL_info = list(old.loc[old['site'] =='Zegveld_Laag'][maps_classes].iloc[1])

#%% create columns for lwH or lwL
lw['site']='lw'
zv['site']='zv'

lw['site'][lw.x_90<150]='lwL'
lw['site'][lw.x_90>=150]='lwH'

zv['site'][zv.x_90<200]='zvH'
zv['site'][zv.x_90>=200]='zvL'
#%% separate dataframes
lwL = lw.iloc[1:3825]
lwH = lw.iloc[3825:]
zvL = zv.iloc[:1900]
zvH = zv.iloc[1901:]
#%% set map values to df's
lwL[maps_classes] = lwL_info
lwH[maps_classes] = lwH_info
zvL[maps_classes] = zvL_info
zvH[maps_classes] = zvH_info

#%%
lw = pd.concat([lwL, lwH])
zv = pd.concat([zvL, zvH])
#%% plot zv and lw
df=air
fig, ax  = plt.subplots(figsize=(8,5))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
#plt.scatter(lw.datetime,lw.x_90, marker='o', s=3)
#plt.scatter(df.datetime, df.NDVI, s=1)
plt.scatter(df.datetime, df.NDVI2, s=1)

plt.gcf().autofmt_xdate()
plt.title('Airborne NDVI')
plt.xlabel('Date')
plt.ylabel('NDVI')
#plt.ylabel('CO2 flux [umol m-2 s-1]')
#plt.ylim(-40,40)
#plt.axhline(y=lw.F_CO2.quantile(0.005), ls='--', color='red', label='99%')
#plt.axhline(y=lw.F_CO2.quantile(0.995), ls='--', color='red')
#plt.legend(loc='upper left')


#plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/NDVI_tower_scatter.png", dpi=300)
#%% Throw out highest 0.5% and lowest 0.5%

lw = lw[(lw['CO2flx'] > lw.CO2flx.quantile(0.005)) & (lw['CO2flx'] < lw.CO2flx.quantile(0.995))]
zv = zv[(zv['CO2flx'] > zv.CO2flx.quantile(0.005)) & (zv['CO2flx'] < zv.CO2flx.quantile(0.995))]

# merge in one dataframe
df = pd.concat([lw, zv])
print(df.isna().sum())
len(df)
df.index = range(len(df))


#%%

df.to_csv(r'C:/Users\l_vdp\Documents\MSc_Thesis\data\preprocessing\towers\DataLangeweideZegveld\lw_zv_99_maps.csv')

#%%plot all data
fig, ax = plt.subplots(figsize=(10,10))
sns.scatterplot(df_9to5.datetime, df_9to5.F_CO2, hue=df.site, linewidth=0)
plt.xlabel('Date')
plt.ylabel('CO2 flux [umol m-2 s-1')
plt.title('Tower data')
#plt.savefig('\content\drive\MyDrive\MSc_Thesis\Figures\CO2_scatter_towers_9to5.png', dpi=300)

#%%


