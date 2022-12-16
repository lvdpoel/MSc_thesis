# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 10:55:52 2022

@author: l_vdp
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from datetime import datetime

#%%
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
#%%
twr  = pd.read_csv(folder_data+'tower_shuffled_3009.csv',
               index_col=0)
air = pd.read_csv(folder_data+'airborne_shuffled_2410.csv',
                 index_col=0)
mer = pd.read_csv(folder_data+'merged_shuffled_2211.csv',
                 index_col=0)
#%%
standard_blue = '#1f77b4'
standard_orange = '#ff7f0e'
standard_green = '#2ca02c'
#%%
LGN_classes = ['Grs', 'SuC', 'SpC', 'Ghs', 'dFr', 'cFr', 'Wat',
       'Bld', 'bSl', 'Hth', 'FnB', 'Shr']
soil_classes = ['hV', 'W', 'pV', 'kV', 'hVz', 'V',
       'Vz', 'aVz', 'kVz', 'overigV', 'zandG', 'zeeK', 'rivK', 'gedA', 'leem']

peat_cls = ['hV', 'W','pV', 'kV', 'hVz', 'V',  'Vz', 'aVz', 'kVz', 'overigV']

all_feats = ['CO2flx', 'PAR_abs', 'Tsfc', 'VPD', 'RH', 'NDVI', 'BBB', 'GWS', 'OWD'] + LGN_classes + soil_classes
#%%
for i in mer.index:
    mer.loc[i, 'Datetime'] = datetime.strptime(str(mer.loc[i, 'Datetime']), '%Y-%m-%d %H:%M:%S')


#%%

sns.set_style("white")
for col in all_feats:
  fig, ax = plt.subplots(figsize=(7,6))
  plt.hist(twr[col], alpha=0.6, label = 'tower',bins=80, color=sns.color_palette()[1])
  plt.hist(air[col], alpha=0.6, label='airborne',bins=80, color = sns.color_palette()[0])
  plt.grid(False)
  plt.legend(title='datatype')
  plt.xlabel(col)
  plt.ylabel('Count')
  plt.title(col)

#%% Stamdard Scale
sc = StandardScaler() 
air_sc = pd.DataFrame(sc.fit_transform(air[all_feats]), columns=all_feats)
twr_sc = pd.DataFrame(sc.fit_transform(twr[all_feats]), columns=all_feats)
#%% Min Max sccale
mm = MinMaxScaler()
air_mm = pd.DataFrame(mm.fit_transform(air[all_feats]), columns=all_feats)
twr_mm = pd.DataFrame(mm.fit_transform(twr[all_feats]), columns=all_feats)

#%%
col = 'Bld'
#%%
plt.hist(air[col], bins=50)
plt.title(col + ' before scaling')
#%%
plt.hist(air_sc.Bld, bins=50)
plt.title( col+ ' with standard scaler')
#%%
plt.hist(air_mm[col], bins=50)
plt.title(col + ' with min max scaler')
#%%
alph = 0.5
for col in all_feats:
    fig, (ax1, ax2, ax3) = plt.subplots(3,1)
    ax1.hist(air[col], bins=70, alpha = alph, label = 'airborne')
    ax1.hist(twr[col], bins=70, alpha=alph, label = 'tower')
    ax1.set_title(col + ' before scaling')
    ax1.legend()
    
    ax2.hist(air_sc[col], bins=70, alpha =alph)
    ax2.hist(twr_sc[col], bins=70, alpha = alph)
    ax2.set_title(col+ ' with standard scaler')
    
    ax3.hist(air_mm[col], bins=70, alpha = alph)
    ax3.hist(twr_mm[col], bins=70, alpha = alph)
    ax3.set_title(col + ' with min max scaler')
#%%,
feats = ['CO2flx', 'PAR_abs','BBB', 'NDVI']
feats2 = ['CO2flx', 'NDVI', 'BBB', 'OWD']

#%%
fig, axs = plt.subplots(2,2,figsize=(6,6))
sns.set_style("white")
for col, ax in zip(feats2, axs.ravel()):
  ax.hist(twr[col], alpha=0.6, label = 'tower',bins=80, color=sns.color_palette()[1])
  ax.hist(air[col], alpha=0.6, label='airborne',bins=80, color = sns.color_palette()[0])
  ax.grid(False)
  #ax.set_legend(title='datatype')
  ax.set_xlabel(col)
  ax.set_ylabel('Count')
  #ax.set_title(col)
#%%
fig, axs = plt.subplots(2,2,figsize=(6,7))
plt.subplots_adjust(hspace=0.5, wspace=0.4)
plt.suptitle("Histograms", fontsize=14, y=0.95)

# loop through the length of tickers and keep track of index
for n, col in enumerate(feats2):
    # add a new subplot iteratively
    ax = plt.subplot(3, 2, n + 1)

    # filter df and plot ticker on the new subplot axis
    ax.hist(twr[col], alpha=0.6, label = 'tower',bins=30, color=sns.color_palette()[1])
    ax.hist(air[col], alpha=0.6, label='airborne',bins=30, color = sns.color_palette()[0])
    ax.grid(False)
    #ax.set_legend(title='datatype')
    ax.set_xlabel(col)
    ax.set_ylabel('Count')
    ax.set_title(col)
    if n == 1:
        ax.legend()
#%%
fig, ((ax1, ax2), (ax3,ax4)) = plt.subplots(2,2, figsize=(6,6))

ax = ax1; col = 'NDVI'
ax.hist(twr[col], alpha=0.6, label = 'tower',bins=10, color=sns.color_palette()[1])
ax.hist(air[col], alpha=0.6, label='airborne',bins=30, color = sns.color_palette()[0])
ax.grid(False)
ax.set_xlabel('NDVI')
ax.set_ylabel('Count')
ax.text(0.2, 1800, 'NDVI', fontdict={'fontweight':'bold'})

ax = ax2; col='GWS'
ax.hist(twr[col], alpha=0.6, label = 'tower',bins=10, color=sns.color_palette()[1])
ax.hist(air[col], alpha=0.6, label='airborne',bins=30, color = sns.color_palette()[0])
ax.grid(False)
ax.set_xlabel('GWS')
ax.text(-1.5, 4200, 'GWS', fontdict={'fontweight':'bold'})


ax=ax3; col='BBB'
ax.hist(twr[col], alpha=0.6, label = 'tower',bins=16, color=sns.color_palette()[1])
ax.hist(air[col], alpha=0.6, label='airborne',bins=30, color = sns.color_palette()[0])
ax.grid(False)
ax.set_xlabel('BBB')
ax.text(330, 1700, 'BBB', fontdict={'fontweight':'bold'})
ax.set_ylabel('Count')

ax=ax4;col='OWD'
ax.hist(twr[col], alpha=0.6, label = 'tower',bins=15, color=sns.color_palette()[1])
ax.hist(air[col], alpha=0.6, label='airborne',bins=30, color = sns.color_palette()[0])
ax.grid(False)
ax.set_xlabel('OWD')
ax.text(3.2, 4200, 'OWD', fontdict={'fontweight':'bold'})

plt.subplots_adjust(hspace=0.3, wspace=0.25)
plt.legend(loc='lower right')
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/hists_4_111_GWS.png', bbox_inches='tight', dpi=300)

#%%
feats = ['CO2flx', 'PAR_abs', 'Tsfc', 'RH','BBB','Grs', 'SpC']
fig, axs = plt.subplots(3,2,figsize=(6,7))
plt.subplots_adjust(hspace=0.5, wspace=0.4)
plt.suptitle("Histograms", fontsize=14, y=0.95)

# loop through the length of tickers and keep track of index
for n, col in enumerate(feats):
    # add a new subplot iteratively
    ax = plt.subplot(3, 2, n + 1)

    # filter df and plot ticker on the new subplot axis
    ax.hist(twr[col], alpha=0.6, label = 'tower',bins=30, color=sns.color_palette()[1])
    ax.hist(air[col], alpha=0.6, label='airborne',bins=30, color = sns.color_palette()[0])
    ax.grid(False)
    #ax.set_legend(title='datatype')
    ax.set_xlabel(col)
    ax.set_ylabel('Count')
    ax.set_title(col)
    if n == 1:
        ax.legend()        
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/hists_6.png', bbox_inches='tight', dpi=300)
#%%
col='NDVI'
fig, ax = plt.subplots(figsize=(4,3))
plt.hist(twr[col], alpha=0.6, label = 'tower',bins=11, color=sns.color_palette()[1])
plt.hist(air[col], alpha=0.6, label='airborne',bins=50, color = sns.color_palette()[0])
plt.grid(False)
plt.legend(title='datatype')
plt.xlabel(col)
plt.ylabel('Count')
plt.title(col)
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/histNDVI.png', bbox_inches='tight', dpi=300)
#%% check if NDVI and LGN classes are correlated. 

LGN_classes_NDVI = ['Grs', 'SuC', 'SpC', 'Ghs', 'dFr', 'cFr', 'Wat',
       'Bld', 'bSl', 'Hth', 'FnB', 'Shr', 'NDVI']
corr = air[LGN_classes_NDVI].corr()

fig = plt.figure(figsize=(13, 9))
ax = fig.add_subplot(111)

cax = ax.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,len(corr.columns),1)
ax.grid(False)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(list(corr.columns), rotation=45,fontdict={'fontsize':9})
ax.set_yticklabels(list(corr.columns), rotation=0, fontdict={'fontsize':9})
plt.title('Correlation matrix all features in merged data', y=1.08)
plt.show()

#%%
for col in LGN_classes:
    fig, ax = plt.subplots(figsize=(7,6))
    plt.scatter(air['NDVI'], air[col], s=0.5)
    plt.title(col)
#%%
plt.scatter(air['NDVI']/0.9, air['Bld'], s=0.5,label='Bld', color='grey')
plt.scatter(air['NDVI']/0.9, air['Grs'], s=0.5, label='Grs', color = 'green')
plt.scatter(twr['NDVI'], twr['Bld'], s=0.5, color='grey')
plt.scatter(twr['NDVI'], twr['Grs'], s=0.5, color='green')
plt.legend(markerscale=4)
plt.xlabel('NDVI')
plt.ylabel('Percentage of land use class')
plt.title('Possible influencers of NDVI')
#%%
#fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/NDVI_Grs_Bld.png', bbox_inches='tight', dpi=300)
#%%
#%% plot PAR, Tsfc, RH to make choices for simulations
#sns.scatterplot(x=mer['PAR_abs'], y=mer['Tsfc'], c=['m'], style=df['marker'])

#%% plot PAR, Tsfc, RH to make choices for simulations

fig, ax=plt.subplots(figsize=(8,5))
markers = {'airborne': '+', 'tower': '.'}

for source, d in mer.groupby('source'):
    plt.scatter(x=d['PAR_abs'], y=d['Tsfc'], c=d['RH'], marker=markers[source], label=source)
plt.legend(loc='lower right', title='datatype')
plt.colorbar(label='RH')
plt.xlim(0,2000)
plt.xlabel('PAR_abs')
plt.ylabel('Tsfc')
plt.title('PAR_abs, Tsfc and RH - merged data')

#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/scatter_PAR_RH_T2.png', bbox_inches='tight', dpi=300)
#%%
mer800 = mer[mer.PAR_abs > 800]
#%%
fig, ax=plt.subplots(figsize=(4,4))
plt.scatter(mer800.Tsfc, mer800.PAR_abs, s=1)
plt.xlabel('Tsfc [°C]')
plt.ylabel('PAR_abs')
plt.title('PAR vs Tsfc \n when PAR>800')
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/PAR_Tsfc_PAR800.png', bbox_inches='tight', dpi=300)
#%% histogram of SpC
fig, ax=plt.subplots()
plt.hist(mer.SpC, bins=100, color='black')
plt.ylim(0,75) #10282 hoogste
plt.text(0.02,70, '10282')
plt.ylabel('Count')
plt.xlabel('% SpC')
plt.title('Histogram of SpC, merged data')
#%%
#fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/hist_spc.png', bbox_inches='tight', dpi=300)
#%%

binary = cm.get_cmap('binary', 10000)
newcolors = binary(np.linspace(0, 15,10000))

newcmp = ListedColormap(newcolors)
#%%
df=mer[mer.soilgroup=='peat']
df = mer.loc[mer['soilclass'].isin(peat_cls)]
#%%
df=mer
#%% Plot OWD, BBB with soil groups
fig, ax=plt.subplots(figsize=(6,4))
sns.scatterplot(df.BBB, df.OWD, hue=df.soilgroup, alpha=0.5, s=13,
                linewidth=0)
plt.xlabel('BBB [mm]')
plt.ylabel('OWD [m -mv]')
plt.title('OWD vs BBB per soil group')  
plt.legend(title='Soil groups', loc='lower right')
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/scatterBBBOWD_soilgroups.png', bbox_inches='tight', dpi=300)

#%%
sns.kdeplot(data=mer,
    x="BBB",
    y="OWD",
    levels=5,
    fill=True,
    alpha=0.6,
    cut=2)

#%%
sns.jointplot(mer.BBB, mer.OWD, kind='kde')

#%%
sns.displot(mer, x='BBB', y='OWD', hue='soilclass',binwidth=(1, 0.01))
#%%
sns.heatmap(x='BBB', y='OWD', hue='soilgroup')
#%%
fig, ax =plt.subplots(figsize=(6,4))
sns.scatterplot(mer.Datetime, mer.CO2flx, hue=mer.source, alpha=0.7)
plt.xticks(rotation=45)
plt.xlabel(None)
plt.ylabel('CO2 flux [umol m-2 s-1]')
plt.legend(title='datatype')
plt.title('Measured CO2 flux from airborne and tower data')
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/scatterCO2_towerairborne.png', bbox_inches='tight', dpi=300)
#%%
fig, ax =plt.subplots(figsize=(6,4))
plt.scatter(mer.BBB, mer.CO2flx, s=3, c=mer.PAR_abs)
plt.xlabel('BBB [mm]')
plt.ylabel('CO2 flux [umol m-2 s-1]')
plt.title('Merged data')
plt.colorbar(label='PAR_abs')
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/scatter_CO2_BBB_merged.png', bbox_inches='tight', dpi=300)


