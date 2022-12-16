# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 19:42:47 2022

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


#%% get data MERGED
mer = pd.read_csv(folder_data+'merged_shuffled_2410.csv',
                 index_col=0)

mer_13feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'SuC', 'SpC', 'Wat', 'dFr', 'rivK', 'pV', 'zeeK', 'V', 'BBB']
mer_13hypp = {'learning_rate': 0.001, 'max_depth': 9, 'n_estimators': 7000, 'subsample': 0.8}
mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']
mer_6hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}

mer_X = mer[mer_6feats]
mer_y = mer['CO2flx']

#%% train model
X = mer_X; y = mer_y; hyperparams = mer_6hypp
#%%
#X = peat_X; y = peat_y; hyperparams = mer_6hypp
# train model on ALL data
# Scale X data
sc = StandardScaler()

X_sc = pd.DataFrame(sc.fit_transform(X), columns=X.columns)

xgbr = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
             max_depth = hyperparams['max_depth'], 
             n_estimators = hyperparams['n_estimators'],
             subsample = hyperparams['subsample'])

xgbr.fit(X_sc, y) 



#%% beatuiful try plot

PAR_values = {'PAR0': 0,'PAR400' : 400, 'PAR800': 800, 'PAR1200' : 1200, 'PAR1600' : 1600}
Tsfc_values = {'T0': 0, 'T5':5 , 'T10':10, 'T15': 15, 'T20':20, 'T25': 25}


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
                 [PAR_values['PAR400'], Tsfc_values['T5']],
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
                 #[PAR_values['PAR1600'], Tsfc_values['T10']],
                 [PAR_values['PAR1600'], Tsfc_values['T15']],
                 [PAR_values['PAR1600'], Tsfc_values['T20']],
                 [PAR_values['PAR1600'], Tsfc_values['T25']]]
#%%
combi_T1520 = [[PAR_values['PAR1200'], Tsfc_values['T15']], 
                 [PAR_values['PAR1200'], Tsfc_values['T20']],
                 [PAR_values['PAR1600'], Tsfc_values['T15']],
                 [PAR_values['PAR1600'], Tsfc_values['T20']],
                 #[PAR_values['PAR800'], Tsfc_values['T15']],
                 #[PAR_values['PAR800'], Tsfc_values['T20']]
                 ]


#%%


colors = sns.color_palette("Paired")
linestyles = ['solid', 'dashdot', 'dashed', 'dotted', (0,(5,10)), (0,(1,10))]
linestyles = [(0,(5,10)), 'dashdot', 'dotted', 'solid', 'dashed',(0,(1,10)) ]
combinations = combi_PAR400
markers = ['o', 'x','o', 'x', 'o', 'x']
#%% PLOT PER PAR!!! 5 PLOTS AND 1 LEGEND plot with colors for PAR nd linestyles for Tsfc

fig, ((ax1, ax2),(ax3,ax4), (ax5, ax6))= plt.subplots(3,2, sharex=False,
                                                      figsize=(8,10))

data= mer
combinations = combi_PAR0
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax1.plot(df['CO2_pred'], ls='solid', linewidth=1,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax1.set_title('PAR = 0')
    ax1.set_ylabel('Predicted CO2 flux')


combinations = combi_PAR400
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax2.plot(df['CO2_pred'], ls='solid', linewidth=1,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax2.set_title('PAR = 400')
    
    
combinations = combi_PAR800
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax3.plot(df['CO2_pred'], ls='solid', linewidth=1,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax3.set_title('PAR = 800')
    ax3.set_ylabel('Predicted CO2 flux')
    ax3.set_ylim(-19,-3)

combinations = combi_PAR1200
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax4.plot(df['CO2_pred'], ls='solid', linewidth=1,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax4.set_title('PAR = 1200')
    ax4.set_xlabel('BBB')
    ax4.set_ylim(-19,-3)


combinations = combi_PAR1600
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax5.plot(df['CO2_pred'], ls='solid', linewidth=1,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax5.set_title('PAR = 1600')
    ax5.set_xlabel('BBB')
    ax5.set_ylabel('Predicted CO2 flux')
    ax5.set_ylim(-19,-3)




ax6.axis('off')
#


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
ax6.legend(handles=legend_elements, bbox_to_anchor=(0.7,0.75))
plt.subplots_adjust(hspace=0.3)

plt.suptitle('CO2 simulations', y=0.93)
#%%
#fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulate_1perPAR.png', bbox_inches='tight', dpi=300)
#%%
#%% PLOT PER PAR AND T1520
legend_PAR = [Line2D([0], [0], label='PAR = 0', ls=linestyles[list(PAR_values).index('PAR0')]),
              Line2D([0], [0], label='PAR = 400',ls=linestyles[list(PAR_values).index('PAR400')]),
              Line2D([0], [0], label='PAR = 800', ls=linestyles[list(PAR_values).index('PAR800')]),
              Line2D([0], [0], label='PAR = 1200', ls=linestyles[list(PAR_values).index('PAR1200')]),
              Line2D([0], [0], label='PAR = 1600',ls=linestyles[list(PAR_values).index('PAR1600')])
 ]
#%% 6 MERGED MODEL HORIZONTAAL GOEIE!!!
fig, ((ax1, ax2,ax3),(ax4, ax5,ax6))= plt.subplots(2,3, sharex=True,
                                                      figsize=(20,10))

data= mer
combinations = combi_PAR0
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax1.scatter(df.index, df['CO2_pred'],s=3,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax1.set_ylabel('Predicted CO2 flux')
    ax1.text(0,17,'PAR = 0', fontdict={'fontweight':'bold'})
    #ax1.text(0,17,'PAR = 0', fontdict={'fontweight':'bold'})

combinations = combi_PAR400
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax2.scatter(df.index,df['CO2_pred'], s=3,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    #ax2.set_title('PAR = 400')
    ax2.text(0,1,'PAR = 400', fontdict={'fontweight':'bold'})

    
# legend_PAR = [#Line2D([0], [0], label='PAR = 0', ls=linestyles[list(PAR_values).index('PAR0')], color='black'),
#               #Line2D([0], [0], label='PAR = 400',ls=linestyles[list(PAR_values).index('PAR400')], color='black'),
#               #Line2D([0], [0], label='PAR = 800', ls=linestyles[list(PAR_values).index('PAR800')], color='black'),
#               #Line2D([0], [0], label='PAR = 1200', ls=linestyles[list(PAR_values).index('PAR1200')], color='black'),
#               #Line2D([0], [0], label='PAR = 1600',ls=linestyles[list(PAR_values).index('PAR1600')], color='black')
#   ]

legend_PAR = [
            Line2D([0], [0], marker ='.', label='PAR_abs = 1200', color='white', markersize=10, markerfacecolor = 'black'),#colors[list(PAR_values).index('PAR1200')]),
            Line2D([0], [0], marker ='^',label='PAR_abs = 1600', color='white', markersize=10, markerfacecolor = 'black')
            ]# colors[list(PAR_values).index('PAR1600')]),
                   
combinations = combi_T1520
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
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
    ax3.legend(handles=legend_PAR, loc='lower right')#, bbox_to_anchor=(1,0.7))
    ax3.text(0,-12.4,'PAR = 1200 and 1600', fontdict={'fontweight':'bold'})

    
combinations = combi_PAR800
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax4.scatter(df.index, df['CO2_pred'],s=3,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax4.set_ylabel('Predicted CO2 flux')
    ax4.set_xlabel('BBB')
    ax4.set_ylim(-19,-3)
    ax4.text(0,-4.5,'PAR = 800', fontdict={'fontweight':'bold'}) 

combinations = combi_PAR1200
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax5.scatter(df.index, df['CO2_pred'],s=3,
              color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax5.set_xlabel('BBB')
    ax5.set_ylim(-19,-3)
    ax5.text(0,-4.5,'PAR = 1200', fontdict={'fontweight':'bold'})



combinations = combi_PAR1600
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax6.scatter(df.index, df['CO2_pred'],s=3,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax6.set_xlabel('BBB')
    ax6.set_ylim(-19,-3)
    ax6.text(0, -4.5, 'PAR = 1600', fontdict={'fontweight':'bold'})







legend_elements = [Line2D([0], [0], marker = 'o', label='Tsfc =  0', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T0')]),
                  Line2D([0], [0],  marker ='o',label='Tsfc = 5', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T5')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 10', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T10')]),
                   Line2D([0], [0],  marker ='o',label='Tsfc = 15', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T15')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 20', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T20')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 25', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T25')]),

                  #  Line2D([0], [0], label='Tsfc = 0', color= colors[list(Tsfc_values).index('T0')]),
                  #  Line2D([0], [0], label='Tsfc = 5',color = colors[list(Tsfc_values).index('T5')]),
                  #  Line2D([0], [0], label='Tsfc = 10', color=colors[list(Tsfc_values).index('T10')]),
                  #  Line2D([0], [0], label='Tsfc = 15', color= colors[list(Tsfc_values).index('T15')]),
                  #  Line2D([0], [0], label='Tsfc = 20', color= colors[list(Tsfc_values).index('T20')]),
                  # Line2D([0], [0], label='Tsfc = 25', color= colors[list(Tsfc_values).index('T25')])]
                  ]
                   


# Create the figure
ax6.legend(handles=legend_elements, loc='upper right')#, bbox_to_anchor=(1,0.8))
plt.subplots_adjust(hspace=0.05)
plt.subplots_adjust(wspace=0.15)
#%%
#fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulate_all_scatter_adjusted.png', bbox_inches='tight', dpi=300)

#%%
df = create_df(0, 20, data)
X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
df['CO2_pred'] = xgbr.predict(X_sc)
maxi=(df['CO2_pred'].max())
mini=(df['CO2_pred'].min())
print(maxi, mini, maxi-mini)
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulate_all.png', bbox_inches='tight', dpi=300)
#%%
fig, ax = plt.subplots()

combinations = combi_T1520
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax.plot(df['CO2_pred'], linewidth=1,
            
             ls =linestyles[list(PAR_values.values()).index(PAR_value)],

                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    #ax3.set_title(None)
    ax.legend(handles=legend_PAR, loc='lower right')#, bbox_to_anchor=(1,0.7))
    ax.text(0,-12.5,'PAR = 1200 and 1600', fontdict={'fontweight':'bold'})
    #%%
    
#fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulate_all_peat.png', bbox_inches='tight', dpi=300)
#%% ADD LINEAR REGRESSION TO PAR = 1200 AND 1600



fig, ax3 = plt.subplots()

combinations = combi_T1520
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    df = create_df(PAR_value, Tsfc_value, data)
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
    ax3.legend(handles=legend_PAR, loc='lower right')#, bbox_to_anchor=(1,0.7))
    ax3.text(0,-12.4,'PAR = 1200 and 1600', fontdict={'fontweight':'bold'})
#
#%%
#fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulate_linregshapley.png', bbox_inches='tight', dpi=300)
#%% big plot with histograms

gridspec = dict(hspace=0.05, height_ratios=[4, 4, 0.4, 4,4],wspace=0.2)
fig, ((ax1, ax2,ax3),(ax1a, ax2a,ax3a), (nv1, nv2, nv3), (ax4, ax5,ax6), (ax4a, ax5a,ax6a) )= plt.subplots(5,3, 
                                                                                         sharex=True,
                                                                                         figsize=(20,25),
                                                                                         gridspec_kw=gridspec)

data= mer
combinations = combi_PAR0
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    mask, df = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax1.scatter(df.index, df['CO2_pred'],s=3,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    ax1.set_ylabel('Predicted CO2 flux')
    #ax1.text(0,17,'PAR = 0', fontdict={'fontweight':'bold'})
    ax1.set_xlim(-5,300)
    ax1.set_ylabel('Predicted CO2 flux [umol m-2 s-1]')
    ax1.set_title('PAR = 0')
    #ax1.text(0,17,'PAR = 0', fontdict={'fontweight':'bold'})
    ax1a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
              alpha=0.5)
    ax1a.set_ylabel('Count')
    ax1a.set_xlabel('BBB [mm]')
    #
    ax1a.tick_params(axis="x", which="both", length=6)
    #ax1a.set_xticks(range(0,301,50))
    #ax1a.xaxis.set_ticklabels(['0', '50', '100', '150', '200', '250', '300'])
    
combinations = combi_PAR400
for i in range(len(combinations)):
    PAR_value = combinations[i][0]; Tsfc_value = combinations[i][1]        
    mask, df  = create_df(PAR_value, Tsfc_value, data)
    X_sc = pd.DataFrame(sc.transform(df[mer_6feats]),columns=mer_6feats)
    df['CO2_pred'] = xgbr.predict(X_sc)
    ax2.scatter(df.index,df['CO2_pred'], s=3,
                 color=colors[list(Tsfc_values.values()).index(Tsfc_value)])
    #ax2.set_title('PAR = 400')
    #ax2.text(0,1,'PAR = 400', fontdict={'fontweight':'bold'})
    ax2.set_ylabel('Predicted CO2 flux [umol m-2 s-1]')
    ax2.set_title('PAR = 400')
    
    ax2a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
              alpha=0.5)
    ax2a.set_ylabel('Count')
    ax2a.set_xlabel('BBB [mm]')

    
# legend_PAR = [#Line2D([0], [0], label='PAR = 0', ls=linestyles[list(PAR_values).index('PAR0')], color='black'),
#               #Line2D([0], [0], label='PAR = 400',ls=linestyles[list(PAR_values).index('PAR400')], color='black'),
#               #Line2D([0], [0], label='PAR = 800', ls=linestyles[list(PAR_values).index('PAR800')], color='black'),
#               #Line2D([0], [0], label='PAR = 1200', ls=linestyles[list(PAR_values).index('PAR1200')], color='black'),
#               #Line2D([0], [0], label='PAR = 1600',ls=linestyles[list(PAR_values).index('PAR1600')], color='black')
#   ]

legend_PAR = [
            Line2D([0], [0], marker ='.', label='PAR_abs = 1200', color='white', markersize=10, markerfacecolor = 'black'),#colors[list(PAR_values).index('PAR1200')]),
            Line2D([0], [0], marker ='^',label='PAR_abs = 1600', color='white', markersize=10, markerfacecolor = 'black')
            ]# colors[list(PAR_values).index('PAR1600')]),
                   
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
    ax3.legend(handles=legend_PAR, loc='lower right')#, bbox_to_anchor=(1,0.7))
    #ax3.text(0,-12.4,'PAR = 1200 and 1600', fontdict={'fontweight':'bold'})
    ax3.set_ylabel('Predicted CO2 flux [umol m-2 s-1]')
    ax3.set_title('PAR = 1200 and 1600')

    ax3a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
              alpha=0.5)
    ax3a.set_ylabel('Count')
    ax3a.set_xlabel('BBB [mm]')

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
    #ax4.text(0,-4.5,'PAR = 800', fontdict={'fontweight':'bold'}) 
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
    #ax5.text(0,-4.5,'PAR = 1200', fontdict={'fontweight':'bold'})
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
    #ax6.text(0, -4.5, 'PAR = 1600', fontdict={'fontweight':'bold'})

    ax6a.hist(mask.BBB, color=colors[list(Tsfc_values.values()).index(Tsfc_value)], 
                   alpha=0.5)
    ax6a.set_ylabel('Count')





legend_elements = [Line2D([0], [0], marker = 'o', label='Tsfc =  0', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T0')]),
                  Line2D([0], [0],  marker ='o',label='Tsfc = 5', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T5')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 10', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T10')]),
                   Line2D([0], [0],  marker ='o',label='Tsfc = 15', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T15')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 20', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T20')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 25', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T25')]),

                  #  Line2D([0], [0], label='Tsfc = 0', color= colors[list(Tsfc_values).index('T0')]),
                  #  Line2D([0], [0], label='Tsfc = 5',color = colors[list(Tsfc_values).index('T5')]),
                  #  Line2D([0], [0], label='Tsfc = 10', color=colors[list(Tsfc_values).index('T10')]),
                  #  Line2D([0], [0], label='Tsfc = 15', color= colors[list(Tsfc_values).index('T15')]),
                  #  Line2D([0], [0], label='Tsfc = 20', color= colors[list(Tsfc_values).index('T20')]),
                  # Line2D([0], [0], label='Tsfc = 25', color= colors[list(Tsfc_values).index('T25')])]
                  ]
                   


# Create the figure
ax6a.legend(handles=legend_elements, loc='upper right')#, bbox_to_anchor=(1,0.8))
ax3a.legend(handles=legend_elements, loc='upper right')#, bbox_to_anchor=(1,0.8))

#plt.subplots_adjust(hspace=0.05)
#plt.subplots_adjust(wspace=0.15)
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/sim_hist_all_titles.png', bbox_inches='tight', dpi=300)
