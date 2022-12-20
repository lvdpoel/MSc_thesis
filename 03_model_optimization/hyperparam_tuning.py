"""
@author: l_vdp

This script looks for the best hyperparameters for the XGBoost model in a grid-mannered
way (using GridSearchCV). Un-comment the dataset hyperparameter should be run for. 
This script needs a long time to run.

Input: Final airborne, tower and merged datasets (.csv). Also, here written in the code,
the selected features after SBFS. 

Output: Textfile with the optimal hyperparameters (.txt).

"""

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost.sklearn import XGBRegressor


#%% save folders names
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
folder_figures = 'C:/Users/l_vdp/Documents/MSc_Thesis/figures/'

#%% Get data airborne
df = pd.read_csv(folder_data+'airborne_final.csv',
                index_col=0)

feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Bld', 'dFr', 'rivK', 'hV', 'zeeK', 'kV', 'W']
y = df['CO2flx']
X = df[feats]
#%% get tower data

# df = pd.read_csv(folder_data+'tower_final.csv',
#                index_col=0)

# feats = ['PAR_abs', 'RH', 'Tsfc', 'NDVI', 'BBB']
# y = df['CO2flx']
# X = df[feats]

#%% get merged data
# df = pd.read_csv(folder_data+'merged_final.csv',
#                 index_col=0)
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

#%% initialize XGBoost
xgb1 = XGBRegressor()

#%% Hyperparameters grid
parameters = {'n_estimators':[750, 1000, 4000,7000],
              'max_depth':[3, 6, 9, 12], 
              'learning_rate':[0.1, 0.05, 0.01, 0.005, 0.001],                      # only for merged added 0.001
              'subsample': [0.55, 0.6, 0.65, 0.7, 0.8, 1]}

#%% prepare Grid Search CV 
xgb_grid = GridSearchCV(xgb1,
                        parameters,
                        verbose=2,
                        cv = 10, 
                        scoring = 'r2'  )

#%% run the grid search (takes long)
xgb_grid.fit(X_train,  y_train)  

#%% print results
print(xgb_grid.best_score_)
print(xgb_grid.best_params_)

#%% get and print scores of these optimal hyperparams
y_pred = xgb_grid.predict(X_test)
print('R2:')
print(r2_score(y_test, y_pred))
print('MSE of the result is:')
print(mean_squared_error(y_test, y_pred))

#%% save results
params = xgb_grid.best_params_

# save best hyperparameters in textfile
text_file = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/airborne_hyperp_1710.txt"
f = open(text_file,"w")

# write file
f.write( str(params) )

# close file
f.close()