# -*- coding: utf-8 -*-
"""
@author: l_vdp

This script creates a dataframe with CO2 simulations for many combinations of PAR and Tsfc.
Future plotting can be easily done using the values from this dataframe.

Input: final merged dataset, and create_df function from prepare_data_for_simulations.py.
Output: dataframe with CO2 predictions for every present combination of PAR and Tsfc
    
"""

#%% some imports

import os
import pandas as pd
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler

os.chdir("C:/Users/l_vdp/Documents/MSc_Thesis/scripts/simulations/")
from prepare_data_for_simulations import create_df
#%% get data

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
mer = pd.read_csv(folder_data+'merged_final.csv',
                 index_col=0)

mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
hyperparams = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}

X = mer[mer_6feats]
y = mer['CO2flx']
#%% train model on ALL data
# Scale X data
sc = StandardScaler()

X_sc = pd.DataFrame(sc.fit_transform(X), columns=X.columns)

xgbr = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
             max_depth = hyperparams['max_depth'], 
             n_estimators = hyperparams['n_estimators'],
             subsample = hyperparams['subsample'])

xgbr.fit(X_sc, y) 
#%% prepare PAR and Tsfc values for which combinations will be created

PAR_values = {'PAR0': 0,'PAR400' : 400, 'PAR800': 800, 'PAR1200' : 1200, 'PAR1600' : 1600}
Tsfc_values = {'T0': 0, 'T5':5 , 'T10':10, 'T15': 15, 'T20':20, 'T25': 25}

#%% create all possible combinations Tsfc and PaAR

combis = []
for PAR in PAR_values.keys():
    for Tsfc in Tsfc_values.keys():
        combis.append(PAR+Tsfc)
        
#%% initialize dataframe

overview_df = pd.DataFrame()

#%% predict for every combination of PAR and Tsfc
# it's possible that a combination is not present, such as PAR=0 and Tsfc=25.
# therefore try ... except is used

# iterate over every PAR and Tsfc value
for PAR in PAR_values.keys():
    for Tsfc in Tsfc_values.keys():
        try:
            
            # dataframe is created 
            mask, df = create_df(PAR_values[PAR], Tsfc_values[Tsfc], mer)
            
            # data is scaled and used to predict
            X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
            CO2_pred = xgbr.predict(X_sc)
            
            # store predictions in dataframe with PAR and Tsfc values as column names
            overview_df[PAR+'_'+Tsfc] = CO2_pred
                        
        except Exception:
            pass
#%%
#overview_df.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/simulations/df_all_simulated_CO2_300.csv")
