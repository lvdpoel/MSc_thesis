"""
Created on Thu Sep 22 10:34:02 2022

@author: l_vdp
"""
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

#%%
folder = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"


# %% get data AIRBORNE
#df = pd.read_csv(folder+'airborne_shuffled_3009.csv',
 #                index_col=0)

# for testing
#test = df[['CO2flx', 'PAR_abs', 'OWD', 'Tsfc',
 #          'NDVI', 'Grs', 'Bld', 'leem', 'hV']].iloc[:1000]
#X = test.drop('CO2flx', axis=1)
#y = test['CO2flx']

first_sel_a = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Grs', 'Bld', 'SuC', 'SpC', 'Wat', 'FnB',
            'dFr', 'rivK', 'hV', 'pV', 'zeeK', 'kV', 'V', 'W', 'BBB'] # misschien ook nog een keer runnen met BBB
# for real
#X = df[first_sel]
#y = df['CO2flx']
#%% get data TOWER
#df = pd.read_csv(folder+'tower_shuffled_3009.csv', index_col=0)

#first_sel = ['PAR_abs', 'RH' ,'Tsfc', 'NDVI', 'OWD', 'BBB']
# for real
#X = df[first_sel]
#y = df['CO2flx']

#%% get dat MERGED
#df = pd.read_csv(folder+'merged_shuffled_3009.csv',
 #               index_col=0)

first_sel_m = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Grs', 'Bld', 'SuC', 'SpC', 'Wat', 'FnB',
         'dFr', 'rivK', 'hV', 'pV', 'zeeK', 'kV', 'V', 'W', 'BBB'] # misschien ook een keer runnen met BBB
# for real
#X = df[first_sel]
#y = df['CO2flx']



#%%



# %% Split in training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.1,
                                                    random_state=123)

# %% Scale
sc = StandardScaler()

X_train_sc = pd.DataFrame(sc.fit_transform(X_train), columns=X_train.columns)
X_test_sc = pd.DataFrame(sc.transform(X_test), columns=X_train.columns)
# %%



# %%
model = XGBRegressor(n_estimators = 1000, learning_rate= 0.05, max_depth=6, subsample=1)
sfs_scoring = 'r2'
# %% function to run SFS

def feature_selection(model, n_features, X_train, y_train):
    sfs1 = SFS(model, k_features=n_features, forward=False, floating=True,
               verbose=2, scoring=sfs_scoring, cv=10)
    sfs1 = sfs1.fit(X_train, y_train)

    best_features = list(sfs1.k_feature_names_)
    best_score = sfs1.k_score_
    return best_features, best_score


# %%
results = {}
metrics = ['mse', 'bias', 'var', 'r2', 'expl_var']
metrics_df = pd.DataFrame(index=range(len(X.columns)), columns=metrics)
#%%
start = datetime.now()
for i in range(4,len(X_train.columns)): 
    n_features=i
    print(i, '/', len(X_train.columns))
    print('sbs function...')
    top_features, score = feature_selection(model, n_features=i, 
                                            X_train = X_train_sc,
                                            y_train = y_train)
    
    # store top features in dict
    results[i] = top_features
    
    X_train_top = X_train_sc[top_features]
    X_test_top = X_test_sc[top_features]
    
    print('fitting model...')
    # fit model with selected features
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
metrics_df.to_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/0910_merged_featsel_metrics_basedonSBSF_r2_mlxtend_BBB_deel1.csv")

# open file for writing
text_file = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/results/0910_merged_feats_basedonSBSF_r2_mlxtend_BBB_deel1.txt"
f = open(text_file,"w")

# write file
f.write( str(results) )

# close file
f.close()
  #%%

plt.plot(metrics_df.index, metrics_df['bias'], label='bias')
plt.plot(metrics_df.index, metrics_df['var'], label='var')
plt.plot(metrics_df.index, metrics_df['mse'], label='mse')
plt.legend()

#plt.title('Metrics of sequential floating backward selection /n airborne data')
plt.xlabel('Number of features')
plt.ylabel('Metric scores')
#%%
plt.plot(metrics_df.index, metrics_df['var'])
plt.title='var'
#%%
plt.plot(metrics_df.index, metrics_df['mse'])
plt.ylim(20,60)
#%%
plt.plot(metrics_df.index, metrics_df['r2'])
plt.title('r2')