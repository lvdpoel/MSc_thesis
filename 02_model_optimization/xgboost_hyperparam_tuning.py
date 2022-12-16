# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:40:35 2022

@author: l_vdp

This script looks for the best hyperparameters for the XGBoost model in a grid-mannered
way (using GridSearchCV)
This script needs a long time to run.
"""

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost.sklearn import XGBRegressor
from datetime import datetime


#%%

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
folder_figures = 'C:/Users/l_vdp/Documents/MSc_Thesis/figures/'
#%%
# Get data airborne
#data = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/airborne/GrHart_0616_preprocessed_v2.csv", index_col=0)
df = pd.read_csv(folder_data+'airborne_shuffled_3009.csv',
                index_col=0)

# # features = ['PAR_abs', 'DoY', 'Tsfc', 'VPD', 'NDVI', 'Grs', 'Bld', 'rivK', 'FnB', 'pV', 'hV', 'Ghs',
# #   'dFr', 'Wat', 'V', 'SuC', 'kV', 'zeeK', 'IIIb', 'Shr', 'cFr', 'IVu', 'IVc', 'GWS',
# #   'VIId', 'SpC', 'Vao', 'BBB', 'IIb', 'VIIIo', 'IIc', 'Ic', 'W', 'gedA', 'zandG', 'Vbd']


# #first_sel = ['PAR_abs','Tsfc', 'NDVI', 'VPD', 'Grs', 'Bld', 'SuC', 'Wat', 'FnB',
#         #     'dFr', 'rivK', 'hV', 'pV','zeeK','kV', 'V', 'W', 'OWD']

# #feats = ['PAR_abs', 'VPD', 'NDVI', 'OWD', 'Grs', 'Tsfc']

feats_0310 = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Bld', 'dFr', 'rivK', 'hV', 'zeeK', 'kV', 'W']
y = df['CO2flx']
X = df[feats_0310]
#%% get tower data

# df = pd.read_csv(folder_data+'tower_shuffled_3009.csv',
#                index_col=0)

# feats = ['PAR_abs', 'RH', 'Tsfc', 'NDVI', 'BBB']
# y = df['CO2flx']
# X = df[feats]

#%% get merged data
# df = pd.read_csv(folder_data+'merged_shuffled_3009.csv',
#                 index_col=0)
# feats_0410 = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Bld', 'SuC', 'SpC', 'rivK', 'hV', 'pV', 'V', 'W', 'OWD']
# feats_1010 = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'SuC', 'SpC', 'Wat', 'dFr', 'rivK', 'pV', 'zeeK', 'V', 'BBB']
# mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
# mer_13feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'SuC', 'SpC', 'Wat', 'dFr', 'rivK', 'pV', 'zeeK', 'V', 'BBB']

# y = df['CO2flx']
# X = df[mer_13feats]
#%%

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=123)

#%%
# Scale X data
sc = StandardScaler()

X_train_sc = pd.DataFrame(sc.fit_transform(X_train), columns=X_train.columns)
X_test_sc = pd.DataFrame(sc.transform(X_test),columns=X_train.columns)

#%%

xgb1 = XGBRegressor()

parameters = {'n_estimators':[750, 1000, 4000,7000],
              'max_depth':[3, 6, 9, 12], 
              'learning_rate':[0.1, 0.05, 0.01, 0.005, 0.001],                      # only for merged added 0.001
              'subsample': [0.55, 0.6, 0.65, 0.7, 0.8, 1]}

#parameters = {'n_estimators':[1000,5000],
 #             'max_depth':[4, 7], # tree complexity,
              #'max_leaves':[4, 8, 20, 30, 50, 75, 100, 150, 200]
  #            'learning_rate':[0.1, 0.01],
   #           'subsample': [0.6, 0.75]
    #}
#%%

xgb_grid = GridSearchCV(xgb1,
                        parameters,
                        verbose=2,
                        cv = 10, 
                        scoring = 'r2'  )

#%%
start = datetime.now()

xgb_grid.fit(X_train,  y_train)  


print(xgb_grid.best_score_)
print(xgb_grid.best_params_)


y_pred=xgb_grid.predict(X_test)

end = datetime.now()

print('R2:')
print(r2_score(y_test, y_pred))
print('MSE of the result is:')
print(mean_squared_error(y_test, y_pred))
print('Execution time is:')
print(end - start)

tower_params = xgb_grid.best_params_

# open file for writing
text_file = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/airborne_hyperp_1710.txt"
f = open(text_file,"w")

# write file
f.write( str(tower_params) )

# close file
f.close()
#%%
# {'learning_rate': 0.001, 'max_depth': 7, 'n_estimators': 5000, 'subsample': 0.65}
# MSE of the result is:
# 43.405355656842694
# Execution time is:
# 11:22:20.678021


#30-09-22 only towers # WRONG FEATURES USED
#{'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 750, 'subsample': 0.55}
#R2:
#0.5785814895423635
#MSE of the result is:
#20.040351360956798
#Execution time is:
#6:58:21.68297

#%%tower correct features

#{'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 750, 'subsample': 0.8}
#R2:
#0.5895722014041438
#MSE of the result is:
#20.356193950447942
#Execution time is:
#8:08:29.835324




## airborne selection 11 features # misschien proberen met nog kleinere learning rate??
#{'learning_rate': 0.005, 'max_depth': 6, 'n_estimators': 750, 'subsample': 0.6}
#R2:
#0.38071929751830913
#MSE of the result is:
#34.40606934729233
