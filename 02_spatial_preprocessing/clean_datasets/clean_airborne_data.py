# -*- coding: utf-8 -*-
"""
@author: l_vdp

Script to prepare airborne data:
- use quality flags
- only keep rows where 0<NDVI<1
- calculate vapour pressure deficit
- check if land use and soil classes sum up to 1
- shuffle data

"""

#%% some imports

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle


#%% get airborne data (already overlaid with spatial info)

rawdata = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne_lgn_soil_owasis_ndvi.csv", index_col=0)

#%% quality flags

# quality flags for CO2 and Ustar, and filters: Ustar>0.15, filter umean<20
data = rawdata[(rawdata['QC_CO2flx'] <= 6) & (rawdata['QC_Ustar'] <= 6) & (rawdata['ustar'] >= 0.15) & (rawdata['umean'] < 20)]
print(len(data))

# also: drop dates 15/5/2020, 2/4/2021 and 23/10/2021 
data = data[(data['Date'] != '2020-05-15') & (data['Date'] != '2021-04-02') & (data['Date'] != '2021-10-23')]
print(len(data))
#%% correct NDCU values

# set all values NDVI lower than 0 to 0
data['NDVI'] = data['NDVI'].where(data['NDVI']>=0, other=0)

data = data[data['NDVI'] <= 1]
#%% calculate VPD and PAR_abs

# create column with vapour pressure deficit (VPD)
data['VPD'] = data['E_sat'] - data['E_act']

# create column with absorbed PAR
data['PAR_abs'] = data['PAR_i'] - data['PAR_r']

#%% drop unnecessary columns

colstodrop = ['Code', 'Time','Label', 'WinLen', 'WinLenGPS', 'WinTime', 
              'StepLen', 'Lon1', 'Lat1', 'Lon2', 'Lat2', 'Alt', 'Lon', 'Lat', 'zm', 
              'wind_dir', 'umean', 'U_', 'V_', 'W_', 'Std_U', 'sigmav', 'Std_W', 'Theta', 
              'P',  'ol','QC_CH4flx', 'QC_filt', 'QC_CO2flx', 'h', 'QC_H', 'QC_LE', 'QC_Ustar',
              'E_act', 'E_act_cm', 'E_sat']
data = data.drop(colstodrop, axis='columns')
#%% overview classes
LGN_classes = ['Grs', 'SuC', 'SpC', 'Ghs', 'dFr', 'cFr', 'Wat',
       'Bld', 'bSl', 'Hth', 'FnB', 'Shr']
soil_classes = ['hV', 'W', 'pV', 'kV', 'hVz', 'V',
       'Vz', 'aVz', 'kVz', 'overigV', 'zandG', 'zeeK', 'rivK', 'gedA', 'leem']

#%% check if sum of land use and soil classes equals to 1
for i in data.index:
  row = data.iloc[i]
  sumLGN = sum(row[LGN_classes])
  print(sumLGN)
  
  sumSOIL = sum(row[soil_classes])
  print(sumSOIL)
  
  plt.scatter(sumLGN, sumSOIL)

#%%
data_shf = shuffle(data)
data_shf.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/airborne_shuffled_2410.csv")