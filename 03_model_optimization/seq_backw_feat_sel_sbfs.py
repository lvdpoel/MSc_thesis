"""
@author: l_vdp

This script performs sequential backward floating selection.

Important for airborne and merged data: SBFS should be run twice, 
once starting with OWD and once starting with BBB.

Input: final datasets airborne, merged and tower (.csv). Also: the pre-selected features
based on correlation and XGBoost feature importance, these are present in the code
and here denoted by first_sel_X.

Output: Dataframe metrics for every subset of features during the SBFS (.csv).  Also, 
a dictionary of all the best features is saved in a textfile (.txt).
These features with corresponding metrics are analysed in 'analyse_metrics_sbfs'.
"""

#%% some imports
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, explained_variance_score
from sklearn.preprocessing import StandardScaler
from mlxtend.evaluate import bias_variance_decomp
import winsound
from datetime import datetime
import matplotlib.pyplot as plt

#%% folder where datasets are
folder = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"

#%% get data TOWER
twr = pd.read_csv(folder+'tower_final.csv', index_col=0)

first_sel_t = ['PAR_abs', 'RH' ,'Tsfc', 'NDVI', 'OWD', 'BBB']
twr_X = twr[first_sel_t]
twr_y = twr['CO2flx']

#%% get data AIRBORNE
air = pd.read_csv(folder+'airborne_final.csv',
                index_col=0)

first_sel_a = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Grs', 'Bld', 'SuC', 'SpC', 'Wat', 'FnB',
            'dFr', 'rivK', 'hV', 'pV', 'zeeK', 'kV', 'V', 'W', 'BBB'] # 'OWD'
air_X = air[first_sel_a]
air_y = air['CO2flx']


#%% get dat MERGED
mer = pd.read_csv(folder+'merged_final.csv',
                index_col=0)

first_sel_m = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Grs', 'Bld', 'SuC', 'SpC', 'Wat', 'FnB',
         'dFr', 'rivK', 'hV', 'pV', 'zeeK', 'kV', 'V', 'W', 'BBB'] # 'OWD'

mer_X = mer[first_sel_m]
mer_y = mer['CO2flx']

#%% Select data to perform SBFS on

X = mer_X; y = mer_y # can be changed to airborne or tower data

#%% Split in training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.1,
                                                    random_state=123)

# %% Scale
sc = StandardScaler()

X_train_sc = pd.DataFrame(sc.fit_transform(X_train), columns=X_train.columns)
X_test_sc = pd.DataFrame(sc.transform(X_test), columns=X_train.columns)


#%% Prepare model with standard hyperparameters
model = XGBRegressor(n_estimators = 1000, learning_rate= 0.05, max_depth=6, subsample=1)
sfs_scoring = 'r2'

#%% function to run sequential backward floating selection

def feature_selection(model, n_features, X_train, y_train):
    sfs1 = SFS(model, k_features=n_features, forward=False, floating=True,
               verbose=2, scoring=sfs_scoring, cv=10)
    sfs1 = sfs1.fit(X_train, y_train)

    best_features = list(sfs1.k_feature_names_)
    best_score = sfs1.k_score_
    return best_features, best_score


#%% Prepare dict to store which features score best each round
# and dataframe to store metrics of the model with these subsets of features

results = {}
metrics = ['mse', 'bias', 'var', 'r2', 'expl_var']
metrics_df = pd.DataFrame(index=range(len(X.columns)), columns=metrics)
#%% run SBFS
start = datetime.now()

# SBFS starts at all features, goes back to 4 features 
# (it is expected that <4 feautres won't perform well)
# Note: for tower data it should be range(1,len(X_train.columns))
for i in range(4,len(X_train.columns)): 
    n_features=i
    print(i, '/', len(X_train.columns))
    print('sbfs function...')
    top_features, score = feature_selection(model, n_features=i, 
                                            X_train = X_train_sc,
                                            y_train = y_train)
    
    # store top features in dict
    results[i] = top_features
    
    # get X with top_features
    X_train_top = X_train_sc[top_features]
    X_test_top = X_test_sc[top_features]
    
    print('fitting model...')
    # fit model with top features
    model.fit(X_train_top, y_train)
    y_pred = model.predict(X_test_top)
    
    # calculate metrics
    r2 = r2_score(y_test, y_pred)
    expl_var = explained_variance_score(y_test,y_pred)
    
    print('bias-variance...')
    # calculate bias-variance trade-off
    mse, bias, var = bias_variance_decomp(model, X_train_top.values, y_train.values, X_test_top.values, y_test.values, loss='mse', num_rounds=200, random_seed=1)
    
    # store metrics in dataframe
    metrics_df.loc[i][metrics] = [mse, bias, var, r2, expl_var]
    
end = datetime.now()
print(end-start)
winsound.Beep(400, 1000)

# save metrics dataframe
metrics_df.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/0910_merged_featsel_metrics_basedonSBSF_r2_mlxtend_BBB_deel1.csv")

# save top features dict as string in textfile
text_file = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/0910_merged_feats_basedonSBSF_r2_mlxtend_BBB_deel1.txt"
f = open(text_file,"w")

# write file
f.write( str(results) )

# close file
f.close()
#%% Now plot the obtained metrics for a quick overview
# Further analysis in 'analyse_metrics_sbfs'
plt.plot(metrics_df.index, metrics_df['bias'], label='bias')
plt.plot(metrics_df.index, metrics_df['var'], label='var')
plt.plot(metrics_df.index, metrics_df['mse'], label='mse')
plt.legend()

plt.title('Metrics of sequential floating backward selection /n airborne data')
plt.xlabel('Number of features')
plt.ylabel('Metric scores')

#%%
plt.plot(metrics_df.index, metrics_df['r2'])
plt.title('r2')