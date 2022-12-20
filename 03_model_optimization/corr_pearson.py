# -*- coding: utf-8 -*-
"""
@author: l_vdp
Script to make Pearson correlation plot for all features with CO2, for all datasets.

Input: Final tower, airborne and merged dataset (.csv).
Output: Pearson correlation plot 
"""

#%% some imports

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% get data

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"

twr  = pd.read_csv(folder_data+'tower_final.csv',
               index_col=0)
air = pd.read_csv(folder_data+'airborne_final.csv',
                 index_col=0)
mer = pd.read_csv(folder_data+'merged_final.csv',
                 index_col=0)

#%% organize features

LGN_classes = ['Grs', 'SuC', 'SpC', 'Ghs', 'dFr', 'cFr', 'Wat',
       'Bld', 'bSl', 'Hth', 'FnB', 'Shr']
soil_classes = ['hV', 'W', 'pV', 'kV', 'hVz', 'V',
       'Vz', 'aVz', 'kVz', 'overigV', 'zandG', 'zeeK', 'rivK', 'gedA', 'leem']
GrWT_classes = ['Ia', 'Ic', 'IIa', 'IIb', 'IIc', 'IIIa', 'IIIb', 'IVc', 'IVu',
       'Vad', 'Vao', 'Vbd', 'Vbo', 'VId', 'VIId', 'VIIId', 'VIIIo', 'VIIo',
       'VIo']

meteo_vars = ['Tsfc', 'VPD', 'PAR_abs']
owasis_vars = ['BBB', 'OWD' , 'GWS']

all_feats = ['CO2flx', 'PAR_abs', 'Tsfc', 'VPD', 'RH', 'NDVI', 'BBB', 'GWS', 'OWD'] + LGN_classes + soil_classes

#%% get correlation, sort and put in one dataframe

airborne_corr = air[all_feats].corr()
tower_corr = twr[all_feats].corr()
merged_corr = mer[all_feats].corr()

ai_corrCO2 = pd.DataFrame(airborne_corr['CO2flx'].sort_values(ascending=False, key=abs))
to_corrCO2 = pd.DataFrame(tower_corr['CO2flx'].sort_values(ascending=False, key=abs))
me_corrCO2 = pd.DataFrame(merged_corr['CO2flx'].sort_values(ascending=False, key=abs))

ai_corrCO2['datatype'] = 'airborne'
to_corrCO2['datatype'] = 'tower'
me_corrCO2['datatype'] = 'merged'

corr_df = pd.concat([ai_corrCO2, to_corrCO2, me_corrCO2]).drop('CO2flx', axis=0).sort_values(by='CO2flx', ascending=False, key=abs)

#%%% Plot Pearson Correlation with CO2 flux

# Visualize
sns.set_style("white")
fig, ax = plt.subplots(figsize=(5,7))
sns.barplot(corr_df.CO2flx, corr_df.index, hue=corr_df.datatype,
            palette=[sns.color_palette()[2], sns.color_palette()[1], sns.color_palette()[0]])
plt.legend(loc='lower right', title='dataype')
plt.title('Pearson Correlation with CO2 flux')
plt.xlabel('Pearson Correlation')
plt.ylabel('Features')
ax.grid(False)

#fig.savefig('/content/drive/MyDrive/MSc_Thesis/Figures/pearson_corr_all.png', bbox_inches='tight', dpi=300, overwrite=True)
