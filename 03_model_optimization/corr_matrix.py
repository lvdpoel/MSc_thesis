"""
@author: l_vdp

Script to make correlation matrix. Paths to datasets can differ.
Select which dataset and featurees correlation matrix should be made for.


Input: Final tower, airborne and merged dataset (.csv).
Output: Correlation matrix for all non-constant features

"""
#%% some imports

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

#%% Select data and features to make corr_matrix for

data = mer[all_feats]

# can also be a subset of features
# data = air[LGN_classes]
# data = twr[owasis_xvars]

#%% drop all constant features (with correlation = NA)
corr = data.corr()
corr = corr.dropna(how='all', axis=1)
corr = corr.dropna(how='all', axis=0)

#%% correlation matrix plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

cax = ax.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,len(corr.columns),1)
ax.grid(False)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(list(corr.columns), rotation=45)
ax.set_yticklabels(list(corr.columns), rotation=0)


#fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/airborne_alldata_corr_matrix.png", dpi=300)




