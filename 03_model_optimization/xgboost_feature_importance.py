"""
@author: l_vdp

This script calculates the feature importances based on the feature selection 
method embedded in XGBoost.

Input: Final twr, air and mer datasets (.csv)
Output: dataframe with all feature importances for all features (.csv),
and a plot visualising these feature importances. 

"""


#%% some imports

import pandas as pd
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#%% get data

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"

twr  = pd.read_csv(folder_data+'tower_final.csv',
               index_col=0)
air = pd.read_csv(folder_data+'airborne_final.csv',
                 index_col=0)
mer = pd.read_csv(folder_data+'merged_final.csv',
                 index_col=0)

#%% overview of features

LGN_classes = ['Grs', 'SuC', 'SpC', 'Ghs', 'dFr', 'cFr', 'Wat',
       'Bld', 'bSl', 'Hth', 'FnB', 'Shr']
soil_classes = ['hV', 'W', 'pV', 'kV', 'hVz', 'V',
       'Vz', 'aVz', 'kVz', 'overigV', 'zandG', 'zeeK', 'rivK', 'gedA', 'leem']

all_feats = ['PAR_abs', 'Tsfc', 'VPD', 'RH', 'NDVI', 'BBB', 'GWS', 'OWD'] + LGN_classes + soil_classes
feature_names=np.array(all_feats)

#%% prepare X and y for every dataset

twr_X = twr[all_feats]
twr_y = twr['CO2flx']

air_X = air[all_feats]
air_y = air['CO2flx']

mer_X = mer[all_feats]
mer_y = mer['CO2flx']

#%% function to get feature importances

def xgboost_fi(X,y):
  
  # scale X data
  sc = StandardScaler()
  X_sc = pd.DataFrame(sc.fit_transform(X), columns=X.columns)

  # fit model on all data with standard hyperparameters
  model = XGBRegressor(n_estimators = 1000, learning_rate= 0.1, max_depth=6, subsample=1)
  model.fit(X_sc, y)

  # feature importances embedded in model:
  feat_imps = model.feature_importances_
  return feat_imps

#%% run function for all datasets

print('getting started...')
twr_imps = xgboost_fi(twr_X,twr_y)
print('second one...')
air_imps = xgboost_fi(air_X, air_y)
print('almost there...')
mer_imps = xgboost_fi(mer_X, mer_y)
print('done!')

#%% organize results

twr_results = pd.DataFrame(columns = ['feat', 'importance', 'datatype'])
twr_results['feat'] = feature_names
twr_results['importance'] = twr_imps
twr_results['datatype'] ='twr'

air_results = pd.DataFrame(columns = ['feat', 'importance', 'datatype'])
air_results['feat'] = feature_names
air_results['importance'] = air_imps
air_results['datatype'] ='air'

mer_results = pd.DataFrame(columns = ['feat', 'importance', 'datatype'])
mer_results['feat'] = feature_names
mer_results['importance'] = mer_imps
mer_results['datatype'] ='mer'

results = pd.concat([air_results, twr_results, mer_results ]).sort_values(by='importance', ascending=False, key=abs)
#%% plot

sns.set_style("white")
fig, ax = plt.subplots(figsize=(5,7))
sns.barplot( x=results.importance, y =results.feat, hue=results.datatype, palette=[sns.color_palette()[2], sns.color_palette()[1], sns.color_palette()[0]])
plt.legend(loc='lower right', title='dataype')
plt.title('Feature importance based on XGBoost')
plt.xlabel('XGBoost Feature Importance')
plt.ylabel('Features')

ax.grid(False)
#fig.savefig('/content/drive/MyDrive/MSc_Thesis/Figures/FI_XGBoost_all.png', bbox_inches='tight', dpi=300, overwrite=True)