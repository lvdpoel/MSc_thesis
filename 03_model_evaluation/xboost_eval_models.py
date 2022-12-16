# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 09:16:58 2022

@author: l_vdp
"""


import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost.sklearn import XGBRegressor
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np

#%%
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
folder_figures = 'C:/Users/l_vdp/Documents/MSc_Thesis/figures/'
#%% tower data

twr = pd.read_csv(folder_data+'tower_shuffled_3009.csv',
               index_col=0)

twr_feats = ['PAR_abs', 'RH', 'Tsfc', 'NDVI', 'BBB']
twr_hypp = {'learning_rate': 0.001, 'max_depth': 9, 'n_estimators': 4000, 'subsample': 0.8}

twr_y = twr['CO2flx']
twr_X = twr[twr_feats]

# %% get data AIRBORNE
air = pd.read_csv(folder_data+'airborne_shuffled_2410.csv',
                 index_col=0)


air_feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Bld', 'dFr', 'rivK', 'hV', 'zeeK', 'kV', 'W']
air_hypp = {'learning_rate': 0.001, 'max_depth': 9, 'n_estimators': 4000, 'subsample': 0.55}

air_X = air[air_feats]
air_y = air['CO2flx']

#%% get data MERGED
mer = pd.read_csv(folder_data+'merged_shuffled_2211.csv',
                 index_col=0)

mer_13feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'SuC', 'SpC', 'Wat', 'dFr', 'rivK', 'pV', 'zeeK', 'V', 'BBB']
mer_13hypp = {'learning_rate': 0.001, 'max_depth': 9, 'n_estimators': 7000, 'subsample': 0.8}
mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
mer_6hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}

mer_4feats = ['PAR_abs', 'Tsfc', 'RH', 'BBB']#, 'NDVI']

mer_X = mer[mer_6feats]
mer_y = mer['CO2flx']
#%%
peat = mer[mer.peat>0.5]

#%%
sbfs_hypp = {'n_estimators': 1000, 'learning_rate': 0.05, 'max_depth':6, 'subsample':1}
test_hypp =  {'n_estimators': 1000, 'learning_rate': 0.3, 'max_depth':6, 'subsample':1}
#%%
def evalmodel(data, feats, hyperparams):
    X = data[feats]
    y = data['CO2flx']
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=0.1, 
                                                       random_state=123)

    
    sc = StandardScaler()

    X_train_sc = pd.DataFrame(sc.fit_transform(X_train), columns=X_train.columns)
    X_test_sc = pd.DataFrame(sc.transform(X_test),columns=X_train.columns)
    
    xgbr = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
                  max_depth = hyperparams['max_depth'], 
                  n_estimators = hyperparams['n_estimators'],
                  subsample = hyperparams['subsample'])
    #xgbr = XGBRegressor(n_estimators = 1000, learning_rate= 0.05, max_depth=3, subsample=0.8)
    
    # to show that you need to do testing and training
   # X_sc = pd.DataFrame(sc.fit_transform(X), columns=X.columns)
    #X_train_sc = X_sc; y_train = y; X_test_sc = X_sc; y_test = y 
    
    xgbr.fit(X_train_sc, y_train)

    y_pred = xgbr.predict(X_test_sc)
    MSE = mean_squared_error(y_test,y_pred)
    R2 = r2_score(y_test,y_pred)
    return MSE, R2, y_pred, y_test

#%%
print('laten we beginnen')
twr_MSE, twr_R2,twr_ypred, twr_ytest  = evalmodel(twr, twr_feats, twr_hypp)
print('goed op weg!')
air_MSE, air_R2, air_ypred, air_ytest = evalmodel(air, air_feats, air_hypp)
print('op de helft nu')
mer_13MSE, mer_13R2, mer_13ypred, mer_13ytest = evalmodel(mer, mer_13feats, mer_13hypp)
print('nog eentje!')
mer_6MSE, mer_6R2, mer_6ypred, mer_6ytest = evalmodel(mer, mer_6feats, mer_6hypp)
print('tadaaa')
#%%
peat_MSE, peat_R2, peat_ypred, peat_ytest = evalmodel(peat, mer_6feats, mer_6hypp)
#%%

#%%

data_noBld = mer[mer.Bld<0.03]
#%%
mer_6MSE, mer_6R2, mer_6ypred, mer_6ytest = evalmodel(mer, ['PAR_abs', 'Tsfc', 'RH', 'OWD', 'Grs', 'NDVI'], sbfs_hypp)



#%%
fig, ax = plt.subplots()
plt.scatter(twr_MSE, twr_R2, label='Tower 5 feats', c='black', marker = 'o', s=100)
plt.scatter(air_MSE, air_R2, label='Airborne 11 feats', c='black', marker = 'v', s=100)
plt.scatter(mer_6MSE, mer_6R2, label = 'Merged 6 feats', c='black', marker = '|', s=100)
plt.scatter(mer_13MSE, mer_13R2, label = 'Merged 13 feats', c='black', marker = '_', s=100)
plt.ylim(0,1)
plt.xlim(15,45)
plt.ylabel('R2')
plt.xlabel('Mean Squared Error')
plt.title('Metrics of four final models with "random_state = 123"')
plt.legend()
#%%
#fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/metrics_final_models_RS123.png', bbox_inches='tight', dpi=300, overwrite=False)


#%%
binary = cm.get_cmap('binary', 256)
newcolors = binary(np.linspace(0, 15,256))
#pink = np.array([248/256, 24/256, 148/256, 1])
#newcolors[:25, :] = pink
newcmp = ListedColormap(newcolors)

plt.hexbin(twr_ytest, twr_ypred, gridsize=(30), cmap = newcmp)
#plt.plot(twr_ytest)
#%%
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

#fig.suptitle('Performance of four models')
plt.subplots_adjust(wspace=0.15, hspace=0.15)
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/preds_final_models_correcthypp_0411_hexbin4.png', bbox_inches='tight', dpi=300)
#%%
#%%
mer.columns
#%%
plt.hist(mer.no_peat, bins=100, alpha=0.5, label='Peat')
plt.hist(mer.peat, bins=100, alpha=0.5, label='No peat')
#plt.ylim(0,1000)
plt.