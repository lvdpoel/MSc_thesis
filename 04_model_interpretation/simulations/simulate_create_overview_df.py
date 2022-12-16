# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 18:53:52 2022

@author: l_vdp
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

os.chdir("C:/Users/l_vdp/Documents/MSc_Thesis/scripts/simulations/")
from prepare_data_for_simulations import create_df
#%%

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
folder_figures = 'C:/Users/l_vdp/Documents/MSc_Thesis/figures/'
#%% get data MERGED
mer = pd.read_csv(folder_data+'merged_shuffled_2410.csv',
                 index_col=0)

mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
mer_6hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}

mer_X = mer[mer_6feats]
mer_y = mer['CO2flx']
#%%
X = mer_X; y = mer_y; hyperparams = mer_6hypp

# train model on ALL data
# Scale X data
sc = StandardScaler()

X_sc = pd.DataFrame(sc.fit_transform(X), columns=X.columns)

xgbr = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
             max_depth = hyperparams['max_depth'], 
             n_estimators = hyperparams['n_estimators'],
             subsample = hyperparams['subsample'])

xgbr.fit(X_sc, y) 
#%%

PAR_values = {'PAR0': 0,'PAR400' : 400, 'PAR800': 800, 'PAR1200' : 1200, 'PAR1600' : 1600}
Tsfc_values = {'T0': 0, 'T5':5 , 'T10':10, 'T15': 15, 'T20':20, 'T25': 25}

#%%

combis = []
for PAR in PAR_values.keys():
    for Tsfc in Tsfc_values.keys():
        combis.append(PAR+Tsfc)
#%%
overview_df = pd.DataFrame()
#%%
min_max_df = pd.DataFrame(columns = list(PAR_values.keys()), index= list(Tsfc_values.keys()))

#%%

for PAR in PAR_values.keys():
    for Tsfc in Tsfc_values.keys():
        try:
            mask, df = create_df(PAR_values[PAR], Tsfc_values[Tsfc], mer)
            X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
            CO2_pred = xgbr.predict(X_sc)
            overview_df[PAR+'_'+Tsfc] = CO2_pred
            min_max_df.loc[Tsfc, PAR] = CO2_pred.max() - CO2_pred.min()
            
        except Exception:
            pass
#%%
overview_df.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/simulations/df_all_simulated_CO2_300.csv")
#%%
for col in overview_df.columns:
    print(col, overview_df[col].max(), overview_df[col].min(), overview_df[col].max() - overview_df[col].min())
#%%
colors = sns.color_palette("Paired")
#%%
fig,ax = plt.subplots()
for i in range(len(min_max_df.columns)):
    col = min_max_df.columns[i]
    plt.plot(min_max_df[col], label=col, color=colors[i+1])
plt.legend()
plt.ylabel('Predicted CO2 max - min')
plt.xlabel('Temperature')
plt.title('Absolute difference in predicted CO2 \n for BBB values 1-200')
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulate_maxmin.png', bbox_inches='tight', dpi=300)
