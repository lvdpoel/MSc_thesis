# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 15:50:32 2022
WAT MOET IK HIER NOG AAN TOEVOEGEN
COMBINEER LGNSOIL EN OWASISNDVI (DOE BIJ DELAATSTE OOK U_ V_ ETC)
CHECK TEMPERATUUR NAAR CELSIUS
ALS KLAAR: MAAK MERGED

@author: l_vdp
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import statistics
import statsmodels.api as sm # Getting acces to statistical models
import statsmodels.formula.api as smf # A convenience interface for specifying models using formula strings and DataFrames
#import scipy.stats as stats
import statsmodels.api as stats

from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.utils import shuffle

from sklearn.metrics import confusion_matrix, mean_squared_error, mean_absolute_percentage_error, r2_score, mean_absolute_error
#%%
# read data and remove NaNs - old Drive paths

#%%
path= "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/GrHart_owasis6.csv"
path = "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/fp_meas_grhart_ndvitest(all).csv"
rawdata = pd.read_csv(path, na_values='-9999', ).drop('comments', axis=1)#.dropna(subset=['CO2flx'])
#%%
rawdata = rawdata.drop(['Unnamed: 0', 'X.1', 'X', 'X.2', 'X.3', 'X.4'], axis=1)
print(rawdata['QC_CO2flx'].value_counts())
print(rawdata['QC_Ustar'].value_counts()) # praktisch alles prima
# print(len(rawdata))

#%%
rawdata = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne_lgn_soil_owasis_ndvi.csv", index_col=0)
#%%
# Quality flags for CO2 and Ustar, and filters: Ustar>0.15, filter umean<20
data = rawdata[(rawdata['QC_CO2flx'] <= 6) & (rawdata['QC_Ustar'] <= 6) & (rawdata['ustar'] >= 0.15) & (rawdata['umean'] < 20)]
print(len(data))

# Also: drop dates 15/5/2020, 2/4/2021 and 23/10/2021 
data = data[(data['Date'] != '2020-05-15') & (data['Date'] != '2021-04-02') & (data['Date'] != '2021-10-23')]
print(len(data))
#%%
# set all values NDVI lower than 0 to 0
# data['NDVI'] = data['NDVI'].where(data['NDVI']>=0, other=0)
# min(data.NDVI)

data = data[data['NDVI'] <= 1]
#%%
# Create column with vapour pressure deficit (VPD)
data['VPD'] = data['E_sat'] - data['E_act']
# Create column with absorbed PAR
data['PAR_abs'] = data['PAR_i'] - data['PAR_r']
#%%
colstodrop = ['Code', 'Time','Label', 'WinLen', 'WinLenGPS', 'WinTime', 
              'StepLen', 'Lon1', 'Lat1', 'Lon2', 'Lat2', 'Alt', 'Lon', 'Lat', 'zm', 
              'wind_dir', 'umean', 'U_', 'V_', 'W_', 'Std_U', 'sigmav', 'Std_W', 'Theta', 
              'P',  'ol','QC_CH4flx', 'QC_filt', 'QC_CO2flx', 'h', 'QC_H', 'QC_LE', 'QC_Ustar',
              'E_act', 'E_act_cm', 'E_sat']
data = data.drop(colstodrop, axis='columns')
#%%

LGN_classes = ['Grs', 'SuC', 'SpC', 'Ghs', 'dFr', 'cFr', 'Wat',
       'Bld', 'bSl', 'Hth', 'FnB', 'Shr']
soil_classes = ['hV', 'W', 'pV', 'kV', 'hVz', 'V',
       'Vz', 'aVz', 'kVz', 'overigV', 'zandG', 'zeeK', 'rivK', 'gedA', 'leem']
GrWT_classes = ['Ia', 'Ic', 'IIa', 'IIb', 'IIc', 'IIIa', 'IIIb', 'IVc', 'IVu',
       'Vad', 'Vao', 'Vbd', 'Vbo', 'VId', 'VIId', 'VIIId', 'VIIIo', 'VIIo',
       'VIo']    
#%%
for i in data.index:
  print(i)
  row = data.iloc[i]
  sumLGN = sum(row[LGN_classes])
  print(sumLGN)
  
  #for cls in LGN_classes:
   # data[cls].loc[i] = data[cls].loc[i]/sumLGN

  sumSOIL = sum(row[soil_classes])
  print(sumSOIL)
  plt.scatter(sumLGN, sumSOIL)
  #for cls in soil_classes:
   # data[cls].loc[i] = data[cls].loc[i]/sumSOIL
  sumGrWT = sum(row[GrWT_classes])
  #for cls in GrWT_classes:
   # data[cls].loc[i] = data[cls].loc[i]/sumGrWT
  print(sumGrWT)
   
#%%
data_shf = shuffle(data)
data_shf.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/airborne_shuffled_2410.csv")