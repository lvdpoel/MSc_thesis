# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 09:16:58 2022

@author: l_vdp
"""


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor, plot_tree, plot_importance
import matplotlib.pyplot as plt
import os
from matplotlib.lines import Line2D
import seaborn as sns


#%%
os.chdir("C:/Users/l_vdp/Documents/MSc_Thesis/scripts/simulations/")
from prepare_data_for_simulations import create_df


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
mer = pd.read_csv(folder_data+'merged_shuffled_2410.csv',
                 index_col=0)

mer_13feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'SuC', 'SpC', 'Wat', 'dFr', 'rivK', 'pV', 'zeeK', 'V', 'BBB']
mer_13hypp = {'learning_rate': 0.001, 'max_depth': 9, 'n_estimators': 7000, 'subsample': 0.8}
mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
mer_6hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}

mer_X = mer[mer_6feats]
mer_y = mer['CO2flx']
#%%
peat  = pd.read_csv(folder_data+'merged_peat99.csv', index_col=0, low_memory=False)
peat_X = peat[mer_6feats]
peat_y = peat['CO2flx']

#%% train model
X = mer_X; y = mer_y; hyperparams = mer_6hypp
#%%
#X = peat_X; y = peat_y; hyperparams = mer_6hypp
#%%
# train model on ALL data
# Scale X data
sc = StandardScaler()

X_sc = pd.DataFrame(sc.fit_transform(X), columns=X.columns)

xgbr = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
             max_depth = hyperparams['max_depth'], 
             n_estimators = hyperparams['n_estimators'],
             subsample = hyperparams['subsample'])

xgbr.fit(X_sc, y) 
#%%
#PAR_values = [0,50, 100]
#PAR_value = 0; Tsfc_value = 5; data=mer
#create_df(PAR_value, Tsfc_value, data)

linestyles = {0: 'solid', 10:'dashed', 20:'dotted'} # based on Tsfc
colors = {0:'blue', 600:'grey', 1200:'red'} # based on PAR

#%% plotjs
# Tsfc_value = 10; data=mer
# PAR_values = [0, 600,1200]
# Tsfc_values = [0,10,20]

#fig, ax = plt.subplots()

#for PAR_value in PAR_values:
    #for Tsfc_value in Tsfc_values:
        
#%%        
#combinations = [[1200,10], [1200,13], [1200,16], [1200,19], [1200,22], [1200, 25]]

#%%
#colors = sns.color_palette("coolwarm", n_colors=len(combinations))   
colors_overv = {0:sns.color_palette("Paired")[1], 
          600:sns.color_palette("Paired")[3], 
          1200:sns.color_palette("Paired")[5]} # based on PAR

#colors = sns.color_palette("hls",6)
linestyles_overv = {0: 'solid', 10:'dashed', 20:'dotted'} # based on Tsfc

#%%

data = peat
#%%
combinations_overv = [[0,0], [0,10], [0,20], [600, 10], [600, 20], [1200,10], [1200,20]]

fig, ax = plt.subplots()

for i in range(len(combinations_overv)):
    PAR_value = combinations_overv[i][0]
    Tsfc_value = combinations_overv[i][1]        
    try:
        df = create_df(PAR_value, Tsfc_value, data)
        X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
        df['CO2_pred'] = xgbr.predict(X_sc)
        plt.plot(df['CO2_pred'], 
                 ls=linestyles_overv[Tsfc_value],
                 color=colors_overv[PAR_value])
    except Exception:
        pass
        
#plt.legend(bbox_to_anchor=(1,0.75), title='(PAR_abs, Tsfc)') 
plt.xlabel('BBB')
plt.ylabel('Predicted CO2 flux')
plt.title('Simulated CO2 based on merged model, peat classes > 99%')

legend_elements = [Line2D([0], [0], marker = 'o', label='PAR_abs =  0', markerfacecolor=colors_overv[0], markersize=10, color='white'),
                   Line2D([0], [0],  marker ='o',label='PAR_abs = 600', markerfacecolor=colors_overv[600], markersize=10, color='white'),
                   Line2D([0], [0], marker = 'o', label='PAR_abs = 1200', markerfacecolor=colors_overv[1200], markersize=10, color='white'),
                   Line2D([0], [0], label='Tsfc = 0', color='black', linestyle = 'solid'),
                   Line2D([0], [0], label='Tsfc = 10', color='black', linestyle= 'dashed'),
                   Line2D([0], [0], label='Tsfc = 20', color='black', linestyle= 'dotted')]


# Create the figure
ax.legend(handles=legend_elements, bbox_to_anchor=(1,0.75))


#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulations_peat.png', bbox_inches='tight', dpi=300)
#%%

# fig, ax= plt.subplots()

# ax.plot(y_pred)
# ax = ax.twinx()
# ax.hist(df['BBB_original'], alpha=0.2, color='grey')
#%%
plot_tree(xgbr, num_trees=0)
#%% second try plot

PAR_values = {'PAR0': 0,'PAR400' : 400, 'PAR800': 800, 'PAR1200' : 1200, 'PAR1600' : 1600}
Tsfc_values = {'T0': 0, 'T5':5 , 'T10':10, 'T15': 15, 'T20':20, 'T25': 25}

#%%
#colors = sns.color_palette("icefire", n_colors=len(PAR_values))   
#colors = sns.color_palette("coolwarm", n_colors=len(PAR_values))   
#colors = sns.diverging_palette(250, 30, l=65, center="dark")
#colors = sns.color_palette("viridis", n_colors=len(PAR_values))
#colors = sns.color_palette("dark:#5A9_r", n_colors=len(PAR_values))
#colors = sns.dark_palette("#69d", reverse=True)

#linestyles = ['solid', 'dashdot', 'dashed', 'dotted', (0,(5,10)), (0,(1,10))]
#%%
fig, ax = plt.subplots()
combinations = [[1200,0], [1200,13]]# [1200,16], [1200,19], [1200,22], [1200, 25]]

#%%
combi_PAR0 = [[PAR_values['PAR0'], Tsfc_values['T0']], 
                 [PAR_values['PAR0'], Tsfc_values['T5']],
                 [PAR_values['PAR0'], Tsfc_values['T10']],
                 [PAR_values['PAR0'], Tsfc_values['T15']],
                 [PAR_values['PAR0'], Tsfc_values['T20']],
                 #[PAR_values['PAR0'], Tsfc_values['T25']]
                 ]
#%%
combi_PAR400 = [#[PAR_values['PAR400'], Tsfc_values['T0']], 
                 #[PAR_values['PAR400'], Tsfc_values['T5']],
                 [PAR_values['PAR400'], Tsfc_values['T10']],
                 [PAR_values['PAR400'], Tsfc_values['T15']],
                 [PAR_values['PAR400'], Tsfc_values['T20']],
                 [PAR_values['PAR400'], Tsfc_values['T25']]]
#%%
combi_PAR800 = [#[PAR_values['PAR1200'], Tsfc_values['T0']], 
                 #[PAR_values['PAR800'], Tsfc_values['T5']],
                 [PAR_values['PAR800'], Tsfc_values['T10']],
                 [PAR_values['PAR800'], Tsfc_values['T15']],
                 [PAR_values['PAR800'], Tsfc_values['T20']],
                 [PAR_values['PAR800'], Tsfc_values['T25']]]
#%%

combi_PAR1200 = [#[PAR_values['PAR1200'], Tsfc_values['T0']], 
                 #[PAR_values['PAR1200'], Tsfc_values['T5']],
                 [PAR_values['PAR1200'], Tsfc_values['T10']],
                 [PAR_values['PAR1200'], Tsfc_values['T15']],
                 [PAR_values['PAR1200'], Tsfc_values['T20']],
                 [PAR_values['PAR1200'], Tsfc_values['T25']]]

#%%
combi_PAR800 = [#[PAR_values['PAR1200'], Tsfc_values['T0']], 
                 #[PAR_values['PAR800'], Tsfc_values['T5']],
                 [PAR_values['PAR800'], Tsfc_values['T10']],
                 [PAR_values['PAR800'], Tsfc_values['T15']],
                 [PAR_values['PAR800'], Tsfc_values['T20']],
                 [PAR_values['PAR800'], Tsfc_values['T25']]]
#%%

combi_PAR1600 = [#[PAR_values['PAR1200'], Tsfc_values['T0']], 
                 #[PAR_values['PAR800'], Tsfc_values['T5']],
                 [PAR_values['PAR1600'], Tsfc_values['T10']],
                 [PAR_values['PAR1600'], Tsfc_values['T15']],
                 [PAR_values['PAR1600'], Tsfc_values['T20']],
                 [PAR_values['PAR1600'], Tsfc_values['T25']]]

#%%
combi_PAR1600 = [#[PAR_values['PAR1200'], Tsfc_values['T0']], 
                 #[PAR_values['PAR800'], Tsfc_values['T5']],
                 [PAR_values['PAR1600'], Tsfc_values['T10']],
                 [PAR_values['PAR1600'], Tsfc_values['T15']],
                 [PAR_values['PAR1600'], Tsfc_values['T20']],
                 [PAR_values['PAR1600'], Tsfc_values['T25']]]


#%%

#colors = sns.color_palette("icefire", n_colors=len(PAR_values))   
#colors = sns.color_palette("coolwarm", n_colors=len(PAR_values))   
#colors = sns.diverging_palette(250, 30, l=65, center="dark")
#colors = sns.color_palette("viridis", n_colors=len(PAR_values))
#colors = sns.color_palette("dark:#5A9_r", n_colors=len(PAR_values))
#colors = sns.dark_palette("#69d", reverse=True)
colors = sns.color_palette("Paired")
#colors = sns.color_palette("hls",6)
linestyles = ['solid', 'dashdot', 'dashed', 'dotted', (0,(5,10)), (0,(1,10))]
combinations = combi_PAR400
#%% plot with colors for PAR nd linestyles for Tsfc

fig, ax = plt.subplots()
for i in range(len(combinations)):
    PAR_value = combinations[i][0]
    Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    plt.plot(df['CO2_pred'], 
                 #ls=linestyles[list(Tsfc_values.values()).index(Tsfc_value)],
                 #ls='solid',
                 #color=colors[list(Tsfc_values.values()).index(Tsfc_value)],
                 color=colors[list(PAR_values.values()).index(PAR_value)],
                
                 linewidth = 1)
    #plt.ylim(-18.5,-3)
        
#plt.legend(bbox_to_anchor=(1,0.75), title='(PAR_abs, Tsfc)') 
plt.xlabel('BBB')
plt.ylabel('Predicted CO2 flux')
plt.title(combinations)


legend_elements = [#Line2D([0], [0], marker = 'o', label='PAR_abs =  0', color='white', markersize=15, markerfacecolor = colors[list(PAR_values).index('PAR0')]),
                  #Line2D([0], [0],  marker ='o',label='PAR_abs = 400', color='white', markersize=15, markerfacecolor = colors[list(PAR_values).index('PAR400')]),
                   #Line2D([0], [0], marker = 'o', label='PAR_abs = 800', color='white', markersize=15, markerfacecolor = colors[list(PAR_values).index('PAR800')]),
                   #Line2D([0], [0],  marker ='o',label='PAR_abs = 1200', color='white', markersize=15, markerfacecolor = colors[list(PAR_values).index('PAR1200')]),
                   #Line2D([0], [0], marker = 'o', label='PAR_abs = 1600', color='white', markersize=15, markerfacecolor = colors[list(PAR_values).index('PAR1600')])]

                   Line2D([0], [0], label='Tsfc = 0', color= colors[list(Tsfc_values).index('T0')]),
                   Line2D([0], [0], label='Tsfc = 5',color = colors[list(Tsfc_values).index('T5')]),
                   Line2D([0], [0], label='Tsfc = 10', color=colors[list(Tsfc_values).index('T10')]),
                   Line2D([0], [0], label='Tsfc = 15', color= colors[list(Tsfc_values).index('T15')]),
                   Line2D([0], [0], label='Tsfc = 20', color= colors[list(Tsfc_values).index('T20')]),
                  Line2D([0], [0], label='Tsfc = 25', color= colors[list(Tsfc_values).index('T25')])]
                   


# Create the figure
ax.legend(handles=legend_elements, bbox_to_anchor=(1.4,0.8))
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulate__T25.png', bbox_inches='tight', dpi=300)
#%%
df = create_df(0, 20, data)
X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
df['CO2_pred'] = xgbr.predict(X_sc)
maxi=(df['CO2_pred'].max())
mini=(df['CO2_pred'].min())
print(maxi, mini, maxi-mini)
