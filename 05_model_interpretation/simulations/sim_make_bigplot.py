"""
@author: l_vdp

This script simulates CO2 fluxes using the optimal merged 6 model and creates
a big figure with six simulations and six corresponding histograms.

This script defines combinations of PAR and Tsfc values. The function create_df
is used to create ataframes with corresponding PAR and Tsfc ranges, average RH, Grs and SpC 
values, and  BBB from 0 to 300. For every subplot of the final big plot, 
the dataframe with combination X is used as data for the model to predict for.
The same combination X is used to create a histogram for in the subplot below.


Input: final merged dataset, and create_df function from prepare_data_for_simulations.py.
Output: big plot with simulations and histograms (also in thesis).


 
"""
#%% some imports

import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import os
from matplotlib.lines import Line2D
import seaborn as sns


#%% import own function

os.chdir("C:/Users/l_vdp/Documents/MSc_Thesis/scripts/simulations/")
from prepare_data_for_simulations import create_df


#%% get data 
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"

mer = pd.read_csv(folder_data+'merged_final.csv',
                 index_col=0)

mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
hyperparams = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}

X = mer[mer_6feats]
y = mer['CO2flx']

#%% train model (on ALL data, no need to split in test and train)

# scale and fit model
sc = StandardScaler()

X_sc = pd.DataFrame(sc.fit_transform(X), columns=X.columns)

xgbr = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
             max_depth = hyperparams['max_depth'], 
             n_estimators = hyperparams['n_estimators'],
             subsample = hyperparams['subsample'])

xgbr.fit(X_sc, y) 

#%% prepare combinations of PAR-string with PAR-value in dictionary

PAR_values = {'PAR0': 0,'PAR400' : 400, 'PAR800': 800, 'PAR1200' : 1200, 'PAR1600' : 1600}
Tsfc_values = {'T0': 0, 'T5':5 , 'T10':10, 'T15': 15, 'T20':20, 'T25': 25}



#%% create sets of combinations with selected values for PAR and Tsfc
# for these combinations, dataframes with features will be created using function create_df
# then, simulations and histograms will be made for every combination

#%%
combi_PAR0 = [[PAR_values['PAR0'], Tsfc_values['T0']], 
                 [PAR_values['PAR0'], Tsfc_values['T5']],
                 [PAR_values['PAR0'], Tsfc_values['T10']],
                 [PAR_values['PAR0'], Tsfc_values['T15']],
                 [PAR_values['PAR0'], Tsfc_values['T20']],
                 ]
#%%
combi_PAR400 = [[PAR_values['PAR400'], Tsfc_values['T5']],
                 [PAR_values['PAR400'], Tsfc_values['T10']],
                 [PAR_values['PAR400'], Tsfc_values['T15']],
                 [PAR_values['PAR400'], Tsfc_values['T20']],
                 [PAR_values['PAR400'], Tsfc_values['T25']]]
#%%
combi_PAR800 = [[PAR_values['PAR800'], Tsfc_values['T10']],
                 [PAR_values['PAR800'], Tsfc_values['T15']],
                 [PAR_values['PAR800'], Tsfc_values['T20']],
                 [PAR_values['PAR800'], Tsfc_values['T25']]]
#%%
combi_PAR1200 = [[PAR_values['PAR1200'], Tsfc_values['T10']],
                 [PAR_values['PAR1200'], Tsfc_values['T15']],
                 [PAR_values['PAR1200'], Tsfc_values['T20']],
                 [PAR_values['PAR1200'], Tsfc_values['T25']]]

#%%
combi_PAR800 = [[PAR_values['PAR800'], Tsfc_values['T10']],
                 [PAR_values['PAR800'], Tsfc_values['T15']],
                 [PAR_values['PAR800'], Tsfc_values['T20']],
                 [PAR_values['PAR800'], Tsfc_values['T25']]]
#%%

combi_PAR1600 = [[PAR_values['PAR1600'], Tsfc_values['T15']],
                 [PAR_values['PAR1600'], Tsfc_values['T20']],
                 [PAR_values['PAR1600'], Tsfc_values['T25']]]
#%%
combi_T1520 = [[PAR_values['PAR1200'], Tsfc_values['T15']], 
                 [PAR_values['PAR1200'], Tsfc_values['T20']],
                 [PAR_values['PAR1600'], Tsfc_values['T15']],
                 [PAR_values['PAR1600'], Tsfc_values['T20']],
                 ]


#%% prepare colors
colors = sns.color_palette("Paired")
#markers = ['o', 'x','o', 'x', 'o', 'x']

#%% create big plot with histograms (also in thesis)

# create grid for plots to be in
gridspec = dict(hspace=0.05, height_ratios=[4, 4, 0.4, 4,4],wspace=0.2)
fig, ((ax1, ax2,ax3), # simulation top row
      (ax1a, ax2a,ax3a), # histograms 
      (nv1, nv2, nv3), # not visible
      (ax4, ax5,ax6), # simulations
      (ax4a, ax5a,ax6a) ) = plt.subplots(5,3, # histograms
                                         sharex=True,
                                         figsize=(20,25),
                                         gridspec_kw=gridspec)

# every sub plot is structured the same way
# in the first subplot I show what has been done

data = mer

# select which combinations of PAR and Tsfc
combinations = combi_PAR0

for i in range(len(combinations)): # looping over combinations

    # select PAR and Tsfc value
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]  
    
    # create dataframe using function        
    mask, df = create_df(PAR_value, Tsfc_value, data)
    
    # scale data and predict
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    
    # ax 1: simulation plot for current combination
    ax1.scatter(df.index, df['CO2_pred'],s=3, 
                # coloris based on index of Tsfc value
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax1.set_ylabel('Predicted CO2 flux')
    ax1.set_xlim(-5,300)
    ax1.set_ylabel('Predicted CO2 flux [umol m-2 s-1]')
    ax1.set_title('PAR = 0')
    
    # ax 1a: histogram plot for current combination
    ax1a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
              alpha=0.5)
    ax1a.set_ylabel('Count')
    ax1a.set_xlabel('BBB [mm]')
    ax1a.tick_params(axis="x", which="both", length=6)
    
combinations = combi_PAR400
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    mask, df  = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax2.scatter(df.index,df['CO2_pred'], s=3,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax2.set_ylabel('Predicted CO2 flux [umol m-2 s-1]')
    ax2.set_title('PAR = 400')
    
    ax2a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
              alpha=0.5)
    ax2a.set_ylabel('Count')
    ax2a.set_xlabel('BBB [mm]')

 # manually create legend
legend_PAR = [
            Line2D([0], [0], marker ='.', label='PAR_abs = 1200', color='white', markersize=10, markerfacecolor = 'black'),#colors[list(PAR_values).index('PAR1200')]),
            Line2D([0], [0], marker ='^',label='PAR_abs = 1600', color='white', markersize=10, markerfacecolor = 'black')
            ]
      
combinations = combi_T1520
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    mask, df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    if PAR_value == 1200:
        marker = '.'
    else: 
        marker = '^'        
    ax3.scatter(df.index, df['CO2_pred'],s=8,
              marker =marker,
                  color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    #ax3.set_title(None)
    ax3.legend(handles=legend_PAR, loc='lower right')
    ax3.set_ylabel('Predicted CO2 flux [umol m-2 s-1]')
    ax3.set_title('PAR = 1200 and 1600')

    ax3a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
              alpha=0.5)
    ax3a.set_ylabel('Count')
    ax3a.set_xlabel('BBB [mm]')

# set center row to not visible
nv1.set_visible(False)
nv2.set_visible(False)    
nv3.set_visible(False)    

    
combinations = combi_PAR800
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    mask, df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax4.scatter(df.index, df['CO2_pred'],s=3,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax4.set_ylabel('Predicted CO2 flux')
    ax4a.set_xlabel('BBB [mm]')
    ax4.set_ylim(-19,-3)
    ax4.set_title('PAR = 800')

    ax4a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
               alpha=0.5)
    ax4a.set_ylabel('Count')
    
    
combinations = combi_PAR1200
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    mask, df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax5.scatter(df.index, df['CO2_pred'],s=3,
              color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax5a.set_xlabel('BBB [mm]')
    ax5.set_ylabel('Predicted CO2 flux [umol m-2 s-1]')
    ax5.set_ylim(-19,-3)
    ax5.set_title('PAR = 1200')

    ax5a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
               alpha=0.5)
    ax5a.set_ylabel('Count')


combinations = combi_PAR1600
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    mask, df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax6.scatter(df.index, df['CO2_pred'],s=3,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax6.set_title('PAR = 1600')
    ax6a.set_xlabel('BBB [mm]')
    ax6.set_ylabel('Predicted CO2 flux [umol m-2 s-1]')
    ax6.set_title('PAR = 1600')

    ax6.set_ylim(-19,-3)

    ax6a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
                   alpha=0.5)
    ax6a.set_ylabel('Count')



# manually create legend elements
legend_elements = [Line2D([0], [0], marker = 'o', label='Tsfc =  0', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T0')]),
                  Line2D([0], [0],  marker ='o',label='Tsfc = 5', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T5')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 10', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T10')]),
                   Line2D([0], [0],  marker ='o',label='Tsfc = 15', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T15')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 20', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T20')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 25', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T25')]),
                  ]
                   

# add legend in two places
ax6a.legend(handles=legend_elements, loc='upper right')
ax3a.legend(handles=legend_elements, loc='upper right')

#%%
#fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/sim_hist_all_titles.png', bbox_inches='tight', dpi=300)
