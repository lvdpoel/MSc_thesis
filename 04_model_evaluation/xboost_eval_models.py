# -*- coding: utf-8 -*-
"""
@author: l_vdp
This script evaluates the final models and produces a plot with the scores.

Input: final airborne, merged and tower dataset (.csv), optimized features and 
hyperparameters, given in the code. 
Output: figure showing the performance of the models
"""


import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost.sklearn import XGBRegressor
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import numpy as np

#%%
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
folder_figures = 'C:/Users/l_vdp/Documents/MSc_Thesis/figures/'
#%% get data TOWER

twr = pd.read_csv(folder_data+'tower_final.csv',
               index_col=0)

twr_feats = ['PAR_abs', 'RH', 'Tsfc', 'NDVI', 'BBB']
twr_hypp = {'learning_rate': 0.001, 'max_depth': 9, 'n_estimators': 4000, 'subsample': 0.8}

twr_y = twr['CO2flx']
twr_X = twr[twr_feats]

# %% get data AIRBORNE

air = pd.read_csv(folder_data+'airborne_final.csv',
                 index_col=0)


air_feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Bld', 'dFr', 'rivK', 'hV', 'zeeK', 'kV', 'W']
air_hypp = {'learning_rate': 0.001, 'max_depth': 9, 'n_estimators': 4000, 'subsample': 0.55}

air_X = air[air_feats]
air_y = air['CO2flx']

#%% get data MERGED

mer = pd.read_csv(folder_data+'merged_final.csv',
                 index_col=0)

mer_13feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'SuC', 'SpC', 'Wat', 'dFr', 'rivK', 'pV', 'zeeK', 'V', 'BBB']
mer_13hypp = {'learning_rate': 0.001, 'max_depth': 9, 'n_estimators': 7000, 'subsample': 0.8}
mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
mer_6hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}


mer_X = mer[mer_6feats]
mer_y = mer['CO2flx']
#%% function to evaluate all models

def evalmodel(data, feats, hyperparams):
    X = data[feats]
    y = data['CO2flx']
    
    # split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=0.1, 
                                                       random_state=123)

    
    # scale
    sc = StandardScaler()

    X_train_sc = pd.DataFrame(sc.fit_transform(X_train), columns=X_train.columns)
    X_test_sc = pd.DataFrame(sc.transform(X_test),columns=X_train.columns)
    
    # model with the correct hyperparameters
    xgbr = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
                  max_depth = hyperparams['max_depth'], 
                  n_estimators = hyperparams['n_estimators'],
                  subsample = hyperparams['subsample'])
    
    # to show that you need to do testing and training, you can also train AND test on the same dataset
    # X_sc = pd.DataFrame(sc.fit_transform(X), columns=X.columns)
    # X_train_sc = X_sc; y_train = y; X_test_sc = X_sc; y_test = y 

    # fit model    
    xgbr.fit(X_train_sc, y_train)
    
    # predict values for test set
    
    # compute scores
    y_pred = xgbr.predict(X_test_sc)
    MSE = mean_squared_error(y_test,y_pred)
    R2 = r2_score(y_test,y_pred)
    return MSE, R2, y_pred, y_test

#%% evaluate all models and store results in variables

twr_MSE, twr_R2,twr_ypred, twr_ytest  = evalmodel(twr, twr_feats, twr_hypp)
air_MSE, air_R2, air_ypred, air_ytest = evalmodel(air, air_feats, air_hypp)
mer_13MSE, mer_13R2, mer_13ypred, mer_13ytest = evalmodel(mer, mer_13feats, mer_13hypp)
mer_6MSE, mer_6R2, mer_6ypred, mer_6ytest = evalmodel(mer, mer_6feats, mer_6hypp)

#%% prepare for hexbin colors

binary = cm.get_cmap('binary', 256)
newcolors = binary(np.linspace(0, 15,256))

newcmp = ListedColormap(newcolors)

#%% Plot figure 
fig, ax = plt.subplots(2,2,sharex=True, sharey=True, figsize=(6,6)) # nog aanpassen miss?

ax[0,0].hexbin(twr_ytest, twr_ypred, gridsize=(20), cmap = newcmp)
ax[0,0].plot(range(-50,50), range(-50,50), '--', c='red')
ax[0,0].set_title('Tower')
ax[0,0].set_ylabel('Predicted CO2')
ax[0,0].text(-47,40, 'R2: '+ str(twr_R2.round(2)))
ax[0,0].text(-47,30, 'MSE: '+ str(twr_MSE.round(1)))


ax[0,1].hexbin(air_ytest, air_ypred, gridsize=(20), cmap = newcmp)
#ax[0,1].scatter(air_ytest, air_ypred, label = 'Airborne', s=10)
ax[0,1].plot(range(-50,50), range(-50,50), '--', c='red')
ax[0,1].set_title('Airborne')
ax[0,1].text(-47,40, 'R2: '+ str(air_R2.round(2)))
ax[0,1].text(-47,30, 'MSE: '+ str(air_MSE.round(1)))


ax[1,0].hexbin(mer_6ytest, mer_6ypred, gridsize=(20), cmap = newcmp)
#ax[1,0].scatter(mer_6ytest, mer_6ypred, label = 'Merged 6', s=10)
ax[1,0].plot(range(-50,50), range(-50,50), '--', c='red')
ax[1,0].set_title('Merged 6')
ax[1,0].set_xlabel('True CO2')
ax[1,0].set_ylabel('Predicted CO2')
ax[1,0].text(-47,40, 'R2: '+ str(mer_6R2.round(2)))
ax[1,0].text(-47,30, 'MSE: '+ str(mer_6MSE.round(1)))


ax[1,1].hexbin(mer_13ytest, mer_13ypred, gridsize=(20), cmap = newcmp)
#ax[1,1].scatter(mer_13ytest, mer_13ypred, label = 'Merged 13', s=10)
ax[1,1].plot(range(-50,50), range(-50,50), '--', c='red')
#ax[1,1].legend(handletextpad=-0.3,handlelength = 0, markerscale=0)
ax[1,1].set_title('Merged 13')
ax[1,1].set_xlabel('True CO2')
ax[1,1].text(-47,40, 'R2: '+ str(mer_13R2.round(2)))
ax[1,1].text(-47,30, 'MSE: '+ str(mer_13MSE.round(1)))

fig.suptitle('Performance of four models')
plt.subplots_adjust(wspace=0.15, hspace=0.15)

#%% save figure

#fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/preds_final_models_correcthypp_0411_hexbin4.png', bbox_inches='tight', dpi=300)
