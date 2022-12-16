# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 15:48:31 2022

@author: l_vdp
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import xgboost
import numpy as np
from datetime import datetime
from scipy.special import expit as sigmoid, logit as inverse_sigmoid

#%%

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
folder_figures = 'C:/Users/l_vdp/Documents/MSc_Thesis/figures/'


#%% get data MERGED
mer = pd.read_csv(folder_data+'merged_shuffled_2211.csv',
                 index_col=0)

mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
hyperparams = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}
#%%

# already correct format:
str_pro = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/knmi/straling_tijdspercentage.csv",
                      sep=',', index_col=0)
#%%
avg_daynight = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/monthly_avg_PAR_daynight.csv",
                  index_col=0)

avg_night = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/monthly_avg_night.csv",
                  index_col=0)

avg = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/monthly_avg.csv",
                  index_col=0)

db_day = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/monthly_avg_debilt_day.csv",
                     index_col=0)
db_night = db_day.copy()
db_night['PAR_abs'] = 0
months = avg_daynight.index
#%%
X_train = mer[mer_6feats]
y_train = mer['CO2flx']

sc = StandardScaler()
#%% OPTION :bootstrap

preds = pd.DataFrame(index=months)
#%%
start = datetime.now()
for it in range(500):
    print(it)
    
    train = mer.sample(frac=0.9, random_state=it)
    X_train = train[mer_6feats]
    y_train = train['CO2flx']
    
    X_train_sc = pd.DataFrame(sc.fit_transform(X_train), columns=X_train.columns)
    db_day_sc = pd.DataFrame(pd.DataFrame(sc.transform(db_day),columns=X_train.columns))
    db_night_sc = pd.DataFrame(pd.DataFrame(sc.transform(db_night),columns=X_train.columns))
    
    xgbr = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
                       max_depth = hyperparams['max_depth'], 
                       n_estimators = hyperparams['n_estimators'],
                       subsample = hyperparams['subsample'])
    xgbr.fit(X_train_sc, y_train)
    y_pred_db_day = xgbr.predict(db_day_sc)
    y_pred_db_night = xgbr.predict(db_night_sc)
    
    preds[it] = (str_pro['De Bilt'] * y_pred_db_day) + ((1-str_pro['De Bilt']) * y_pred_db_night)
end = datetime.now()
print(end-start)

#%%
preds.T.boxplot()
#%%
preds.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/preds_500bootstrap.csv")
#%%
stds = []
for month in months:
    std = (preds.T)[month].std()
    print(month, std)
    stds.append(std)

avg_std = sum(stds)/len(stds) #0.4392244516097776
#%%









