# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 11:13:56 2022

@author: l_vdp
Script to make correlation matrices and pearson correlation plot, for airborne, 
tower and merged data.
Downloaded from Jupyter Notebook, so be aware paths to datasets can differ.

"""
#%% some imports

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math


#%% get data
airborne = pd.read_csv('/content/drive/MyDrive/GrHart_0616_preprocessed_v2.csv', index_col=0)

tower = pd.read_csv('/content/drive/MyDrive/MSc_Thesis/Data/Towers/towers_2409.csv', index_col=0)

merged = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/merged_2809.csv", index_col=0)


#%%
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
#%%
twr  = pd.read_csv(folder_data+'tower_shuffled_3009.csv',
               index_col=0)
air = pd.read_csv(folder_data+'airborne_shuffled_2410.csv',
                 index_col=0)
mer = pd.read_csv(folder_data+'merged_shuffled_2410.csv',
                 index_col=0)

airborne = air; tower = twr; merged = mer
#%% organize features
LGN_classes = ['Grs', 'SuC', 'SpC', 'Ghs', 'dFr', 'cFr', 'Wat',
       'Bld', 'bSl', 'Hth', 'FnB', 'Shr']
soil_classes = ['hV', 'W', 'pV', 'kV', 'hVz', 'V',
       'Vz', 'aVz', 'kVz', 'overigV', 'zandG', 'zeeK', 'rivK', 'gedA', 'leem']
GrWT_classes = ['Ia', 'Ic', 'IIa', 'IIb', 'IIc', 'IIIa', 'IIIb', 'IVc', 'IVu',
       'Vad', 'Vao', 'Vbd', 'Vbo', 'VId', 'VIId', 'VIIId', 'VIIIo', 'VIIo',
       'VIo']

all_feats = ['CO2flx', 'PAR_abs', 'Tsfc', 'VPD', 'RH', 'NDVI', 'BBB', 'GWS', 'OWD'] + LGN_classes + soil_classes

#%% FOR ONLY TOWER DATA
data = merged[all_feats]
#%%% for only owasis
meteo_vars = ['Tsfc', 'VPD', 'PAR_abs']
owasis_vars = ['BBB', 'OWD' , 'GWS']
#data = data[owasis_vars]

#%%% for all changing tower variables
corr = data.corr()
corr = corr.dropna(how='all', axis=1)
corr = corr.dropna(how='all', axis=0)
#%%% correlation matrix plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

cax = ax.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,len(data.columns),1)
ax.grid(False)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(list(data.columns), rotation=45)
ax.set_yticklabels(list(data.columns), rotation=0)
#fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/airborne_alldata_corr_matrix.png", dpi=300)

#%%% pearson plot
fig,ax=plt.subplots(figsize=(5,5))
corr_df = data.corr(method='pearson')
plt.figure(figsize=(8, 6))
sns.heatmap(corr_df, annot=True,vmin=-1, vmax=1,cmap= 'coolwarm')
plt.title('Correlation between OWASIS variables /n (airborne data)')
plt.tight_layout()
#plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/airborne_alldata_corr_matrix_owasis.png", dpi=300)
#%% FOR ALL DATA
#%%% get correct columns
columns = ['CO2flx','Tsfc', 'RH', 'NDVI', 'Grs', 'SuC', 'SpC',
       'Ghs', 'dFr', 'cFr', 'Wat', 'Bld', 'bSl', 'Hth', 'FnB', 'Shr', 'hV',
       'W', 'pV', 'kV', 'hVz', 'V', 'Vz', 'aVz', 'kVz', 'overigV', 'zandG',
       'zeeK', 'rivK', 'gedA', 'leem', 'BBB', 'GWS', 'OWD', 'VPD', 'PAR_abs']

#%%% get correlation, sort and organize
airborne_corr = airborne[columns].corr()
tower_corr = tower[columns].corr()
merged_corr = merged[columns].corr()

ai_corrCO2 = pd.DataFrame(airborne_corr['CO2flx'].sort_values(ascending=False, key=abs))
to_corrCO2 = pd.DataFrame(tower_corr['CO2flx'].sort_values(ascending=False, key=abs))
me_corrCO2 = pd.DataFrame(merged_corr['CO2flx'].sort_values(ascending=False, key=abs))

ai_corrCO2['datatype'] = 'airborne'
to_corrCO2['datatype'] = 'tower'
me_corrCO2['datatype'] = 'merged'

corr = pd.concat([ai_corrCO2, to_corrCO2, me_corrCO2]).drop('CO2flx', axis=0).sort_values(by='CO2flx', ascending=False, key=abs)
#%%% plot pearson corr
# Visualize
sns.set_style("white")
fig, ax = plt.subplots(figsize=(5,7))
sns.barplot(corr.CO2flx, corr.index, hue=corr.datatype,
            palette=[sns.color_palette()[2], sns.color_palette()[1], sns.color_palette()[0]])
plt.legend(loc='lower right', title='dataype')
plt.title('Pearson Correlation with CO2 flux')
plt.xlabel('Pearson Correlation')
plt.ylabel('Features')
ax.grid(False)
#fig.savefig('/content/drive/MyDrive/MSc_Thesis/Figures/pearson_corr_all.png', bbox_inches='tight', dpi=300, overwrite=True)
#%% HISTOGRAMS ALL DATA
sns.set_style("white")

fig, ax = plt.subplots(figsize=(7,6))
plt.hist(merged.CO2flx, alpha=0.7, label = 'merged', bins=20, color=sns.color_palette()[2])
plt.hist(tower.CO2flx, alpha=0.7, label = 'tower', bins=20, color=sns.color_palette()[1])
plt.hist(airborne.CO2flx, alpha=0.7, label='airborne', bins=20, color = sns.color_palette()[0])
plt.grid(False)
plt.legend(title='datatype')
plt.title('Histogram of CO2 flux data')
#fig.savefig('/content/drive/MyDrive/MSc_Thesis/Figures/hist_all.png', bbox_inches='tight', dpi=300, overwrite=True)