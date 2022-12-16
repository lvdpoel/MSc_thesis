# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 17:36:10 2022

@author: l_vdp
"""

# NOG NIET GEDAAN MISSCHIEN HANDIG MAAR HIER GEPRUTS

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost.sklearn import XGBRegressor
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np
from matplotlib import dates as mdates
from matplotlib import ticker

#%%%

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
folder_figures = 'C:/Users/l_vdp/Documents/MSc_Thesis/figures/'


#%% get data MERGED
mer = pd.read_csv(folder_data+'merged_shuffled_2211.csv',
                 index_col=0)

mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
mer_6hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}



#%%

for i in mer.index:
    dat = mer.loc[i, 'Datetime']
    mer.loc[i, 'datetime'] = datetime.strptime(str(dat), '%Y-%m-%d %H:%M:%S')
#%%

mer[pd.DatetimeIndex(mer['datetime']).date == datetime.date(2021, 11, 22)]

#%%
date1 = '2020-06-09'
date2 = '2021-09-16'

mer_test = mer[mer['Datetime'].str.contains(date1)]
#mer_test = mer.head(500)
#%%
#X =  mer[mer_6feats]
#y = mer['CO2flx']


#%%
X_train = mer[mer_6feats]
y_train = mer['CO2flx']
X_test = mer_test[mer_6feats]
y_test = mer_test['CO2flx']

#%%
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, 
 #                                                   random_state=123)

sc = StandardScaler()

X_train_sc = pd.DataFrame(sc.fit_transform(X_train), columns=X_train.columns)
X_test_sc = pd.DataFrame(sc.transform(X_test),columns=X_train.columns)

hyperparams = mer_6hypp 
xgbr = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
               max_depth = hyperparams['max_depth'], 
               n_estimators = hyperparams['n_estimators'],
               subsample = hyperparams['subsample'])
 

xgbr.fit(X_train_sc, y_train)
y_pred = xgbr.predict(X_test_sc)
#%%
fig, ax = plt.subplots()

plt.scatter(mer_test.datetime, y_pred, label='Predicted', s=5, color='red')
plt.scatter(mer_test.datetime, mer_test.CO2flx, label='True', s=5, color='black')
plt.legend()
plt.title('True and predicted CO2 for '+ date1)
plt.xticks(rotation=45)
plt.ylabel('CO2 flux [umol m-2 s-1]')

# Set X range. Using left and right variables makes it easy to change the range.
#
left = date(2020, 2, 1)
right = date(2022, 1, 31)
# Format the date into months & days
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) 

# Change the tick interval
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=4)) 

# Puts x-axis labels on an angle
plt.gca().xaxis.set_tick_params(rotation = 30)  

# Changes x-axis range
#plt.gca().set_xbound(left, right)
#%%
#fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/pred_true_1122.png", dpi=300)

#%%

fig, ax = plt.subplots()

plt.scatter(mer_test.index, y_pred, label='Predicted', s=5, color='red')
plt.scatter(mer_test.index, mer_test.CO2flx, label='True', s=5, color='black')
plt.legend()
plt.title('True and predicted CO2 for '+ date1)
plt.xticks(None)

plt.ylabel('CO2 flux [umol m-2 s-1]')
#%%
fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/pred_true_0609.png", dpi=300)

