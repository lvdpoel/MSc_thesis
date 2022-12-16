#%% some imports
import pandas as pd
from xgboost import XGBRegressor, plot_importance
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, log_loss
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#%% preparation
all_feats = ['PAR_abs', 'Tsfc', 'VPD', 'RH', 'NDVI', 'BBB', 'GWS', 'OWD'] + LGN_classes + soil_classes
feature_names=np.array(all_feats)
#%% get data
tower = pd.read_csv('/content/drive/MyDrive/MSc_Thesis/Data/Towers/towers_2409.csv', index_col=0)
tower_X = tower[all_feats]
tower_y = tower['CO2flx']

airborne = pd.read_csv('/content/drive/MyDrive/MSc_Thesis/Data/Airborne/GrHart_0616_preprocessed.csv', index_col=0)
airborne_X = airborne[all_feats]
airborne_y = airborne['CO2flx']

merged = pd.read_csv('/content/drive/MyDrive/MSc_Thesis/Data/merged_2809.csv', index_col=0)
merged_X = merged[all_feats]
merged_y = merged['CO2flx']
#%% function to get feature importances
def xgboost_fi(X,y):
  
  # Scale
  sc = StandardScaler()

  X_sc = pd.DataFrame(sc.fit_transform(X), columns=X.columns)

  # fit model on all training data
  model = XGBRegressor(n_estimators = 1000, learning_rate= 0.1, max_depth=6, subsample=1)
  model.fit(X_sc, y)

  feat_imps = model.feature_importances_
  return feat_imps

#%% run for all datasets
print('getting started...')
tower_imps = xgboost_fi(tower_X,tower_y)
print('second one....')
airborne_imps = xgboost_fi(airborne_X, airborne_y)
print('almost there....')
merged_imps = xgboost_fi(merged_X, merged_y)
print('done!')
#%% organize results
tower_results = pd.DataFrame(columns = ['feat', 'importance', 'datatype'])
tower_results['feat'] = feature_names
tower_results['importance'] = tower_imps
tower_results['datatype'] ='tower'

airborne_results = pd.DataFrame(columns = ['feat', 'importance', 'datatype'])
airborne_results['feat'] = feature_names
airborne_results['importance'] = airborne_imps
airborne_results['datatype'] ='airborne'

merged_results = pd.DataFrame(columns = ['feat', 'importance', 'datatype'])
merged_results['feat'] = feature_names
merged_results['importance'] = merged_imps
merged_results['datatype'] ='merged'

results = pd.concat([airborne_results, tower_results, merged_results ]).sort_values(by='importance', ascending=False, key=abs)
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