# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 10:12:04 2022

@author: l_vdp
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
#%% tower
#path = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/2609_tower_featsel_metrics_basedonSBSF_r2_mlxtend.csv"
#feats={1: ['PAR_abs'], 2: ['PAR_abs', 'OWD'], 3: ['PAR_abs', 'RH', 'OWD'], 4: ['PAR_abs', 'RH', 'OWD', 'Grs'], 5: ['PAR_abs', 'RH', 'NDVI', 'OWD', 'Grs'], 6: ['PAR_abs', 'VPD', 'RH', 'NDVI', 'OWD', 'Grs'], 7: ['PAR_abs', 'VPD', 'RH', 'Tsfc', 'NDVI', 'OWD', 'Grs']}

# second version
path = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/featsel_mlxtend/tower/3009_tower_featsel_metrics_basedonSBSF_r2_mlxtend.csv"
tower = pd.read_csv(path, index_col=0)
#feats = {1: ['PAR_abs'], 2: ['PAR_abs', 'BBB'], 3: ['PAR_abs', 'RH', 'BBB'], 4: ['PAR_abs', 'RH', 'NDVI', 'BBB'], 5: ['PAR_abs', 'RH', 'Tsfc', 'NDVI', 'BBB']}
#%% airborne

airborneOWDpath = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/featsel_mlxtend/airborne/0110_airborne_featsel_metrics_basedonSBSF_r2_mlxtend_OWD.csv"
airborneBBBpath = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/featsel_mlxtend/airborne/0210_airborne_featsel_metrics_basedonSBSF_r2_mlxtend_BBB.csv"
airborneOWD =pd.read_csv(airborneOWDpath, index_col=0)
airborneBBB = pd.read_csv(airborneBBBpath, index_col=0)

#%% merged OWD
merged1_path = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/0410_merged_featsel_metrics_basedonSBSF_r2_mlxtend_OWD_deel1.csv"
merged2_path = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/0410_merged_featsel_metrics_basedonSBSF_r2_mlxtend_OWD_deel2.csv"

merged1 = pd.read_csv(merged1_path, index_col=0).dropna(axis=0)
merged2 = pd.read_csv(merged2_path, index_col=0).dropna(axis=0)

merged = pd.concat([merged1, merged2])
merged.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/featsel_mlxtend/0410_merged_featsel_metrics_basedonSBSF_r2_mlxtend_OWD.csv")
#%% merged OWD
mergedOWD = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/featsel_mlxtend/merged/0410_merged_featsel_metrics_basedonSBSF_r2_mlxtend_OWD.csv", index_col=0)
#%% merged BBB
mergedBBB = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/featsel_mlxtend/merged/0910_merged_featsel_metrics_basedonSBSF_r2_mlxtend_BBB.csv", index_col=0).dropna(axis=0)

#%%

#plt.plot(mergedBBB.r2, label = 'OWD')
#plt.plot(mergedBBB.r2, label = 'BBB')
# plt.legend()
#%%
df  = mergedBBB
#%%
plt.plot(df['r2'], label='r2')
plt.legend()
#%%
plt.plot(df['mse'], label = 'mse')
plt.plot(df['var'], label = 'var')
plt.plot(df['bias'], label = 'bias')
plt.legend()
#%%

fig, ax = plt.subplots()

ax.plot(df['r2'], label='R2', color='black')
ax.set_ylabel('R2 score')
ax.set_xlabel('Number of features')
ax.set_ylim(0.56,0.61)
ax2 = ax.twinx()
ax2.plot(df['mse'], label='MSE')
ax2.plot(df['var'], label='Var')
ax2.plot(df['bias'], label='Bias')
ax2.set_ylabel('MSE, Var, bias score')

plt.title('Metrics of SBFS - merged data (with OWD)')
fig.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/metrics_sbfs_merged_OWD.png', bbox_inches='tight', dpi=300, overwrite=False)
#%%
# select 11 features    
standard_blue = '#1f77b4'
standard_orange = '#ff7f0e'
standard_green = '#2ca02c'
#%% now with two datasets
fig, ax = plt.subplots()

ax.plot(mergedBBB['r2'], label='R2', color='black')
ax.plot(mergedOWD['r2'], color='black', linestyle='--')
ax.set_ylabel('R2 score')
ax.set_xlabel('Number of features')
ax2 = ax.twinx()
#BBB df
ax2.plot(mergedBBB['mse'], label='MSE', color = standard_blue)
ax2.plot(mergedBBB['var'], label='Var', color = standard_orange)
ax2.plot(mergedBBB['bias'], label='Bias', color = standard_green)

# OWD df
ax2.plot(mergedOWD['mse'], linestyle='--', color = standard_blue)
ax2.plot(mergedOWD['var'], linestyle='--', color = standard_orange)
ax2.plot(mergedOWD['bias'], linestyle='--', color = standard_green)
ax2.set_ylabel('MSE, Var, bias score')
ax2.set_ylim(-5,55)

plt.title('Metrics of SBFS - merged data')
fig.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/metrics_sbfs_merged_BBB_OWDdashed.png', bbox_inches='tight', dpi=300, overwrite=False)
#%% 3 subplots in 1
fig, (ax1a, ax2a, ax3a) = plt.subplots(3,1, figsize=(7,10))

# FIRST PLOT
ax1a.plot(tower['r2'], color='black', label= 'R2')
ax1a.set_ylabel('R2 score')
ax1a.set_xlabel('Number of features')
ax1a.text(2.7,0.465, 'Tower data', weight='bold').set_backgroundcolor('white')
ax1b = ax1a.twinx()
ax1b.plot(tower['mse'], color=standard_blue, label='MSE')
ax1b.plot(tower['var'], color=standard_orange, label='Var')
ax1b.plot(tower['bias'], color=standard_green, label = 'Bias')
ax1b.set_ylabel('MSE, Var, bias score')
ax1b.set_ylim(0,45)
#ax1a.legend()
#fig.legend(loc='center right')
#plt.title('Tower data')

legend_elements = [Line2D([0], [0], label='R2', color='black'),
                   Line2D([0], [0], label='MSE', color=standard_blue),
                   Line2D([0], [0], label='Bias', color=standard_green),
                   Line2D([0], [0], label='Var', color=standard_orange)]

ax1b.legend(handles=legend_elements, loc='upper left')

# SECOND PLOT
ax2a.plot(airborneBBB['r2'], color='black')
ax2a.plot(airborneOWD['r2'], color='black', linestyle='--')
ax2a.set_ylabel('R2 score')
ax2a.set_xlabel('Number of features')
ax2a.set_ylim(0.18,0.3)
ax2a.text(10,0.29, 'Airborne data', weight='bold').set_backgroundcolor('white')

ax2b = ax2a.twinx()

#plt.title('Airborne data')

#BBB df
ax2b.plot(airborneBBB['mse'],color = standard_blue)
ax2b.plot(airborneBBB['var'],color = standard_orange)
ax2b.plot(airborneBBB['bias'],color = standard_green)
# OWD df
ax2b.plot(airborneOWD['mse'], linestyle='--', color = standard_blue)
ax2b.plot(airborneOWD['var'], linestyle='--', color = standard_orange)
ax2b.plot(airborneOWD['bias'], linestyle='--', color = standard_green)
ax2b.set_ylabel('MSE, Var, bias score')
ax2b.set_ylim(-5,60)


# THIRD PLOT
ax3a.plot(mergedBBB['r2'], label='R2', color='black')
ax3a.plot(mergedOWD['r2'], color='black', linestyle='--')#label = 'R2 with OWD', 
ax3a.set_ylabel('R2 score')
ax3a.set_xlabel('Number of features')
ax3a.set_ylim(0.55,0.61)
ax3b = ax3a.twinx()
ax3a.text(10,0.605, 'Merged data', weight='bold').set_backgroundcolor('white')

#BBB df
ax3b.plot(mergedBBB['mse'], label='MSE', color = standard_blue)
ax3b.plot(mergedBBB['var'], label='Var', color = standard_orange)
ax3b.plot(mergedBBB['bias'], label='Bias', color = standard_green)

# OWD df
ax3b.plot(mergedOWD['mse'], linestyle='--', color = standard_blue) #label = 'MSE with OWD', 
ax3b.plot(mergedOWD['var'], linestyle='--', color = standard_orange) # label='Var with OWD', 
ax3b.plot(mergedOWD['bias'], linestyle='--', color = standard_green)# label = 'Bias with OWD', 
ax3b.set_ylabel('MSE, Var, bias score')
ax3b.set_ylim(-5,40)

#plt.title('Merged data')
#fig.legend(bbox_to_anchor=(0.5, 0))
fig.subplots_adjust(wspace=0.13, hspace=0.4)

legend_elements = [Line2D([0], [0], label='OWD', color='black', ls = 'dashed'),
                   Line2D([0], [0], label='BBB', color='black', ls = 'solid')]
                  
                   


# Create the figure
ax3b.legend(handles=legend_elements, loc='center right')#, bbox_to_anchor=(1,0.8))

#ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/metrics_alls_sbfs_3_short3.png', bbox_inches='tight', dpi=300, overwrite=False)

