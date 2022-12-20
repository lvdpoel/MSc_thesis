# -*- coding: utf-8 -*-
"""
@author: l_vdp

This model performs the shapley analysis on the four best performing models.
A number of possible plots is shown. Also, a big plot is made with 6 subplots (see thesis).
At the end of the script, linear regression is done on shapley values 
for an explained subset of the dataset where PAR_abs > 80. 
Linear regression is run for 90<BBB<150.

Input: final tower datasets
Output: All shapley plots: beeswarm (overview figure), single scatterplot of choice,
a big figure with 6 subplots, and the linear regression plot.

Data for shapley analysis should be selected (i.e. choosing airborne, merged or tower).
"""


#%%
import pandas as pd
import shap
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf # A convenience interface for specifying models using formula strings and DataFrames


#%% get data

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
folder_figures = 'C:/Users/l_vdp/Documents/MSc_Thesis/figures/'
#%% tower data

twr = pd.read_csv(folder_data+'tower_final.csv',
               index_col=0)

twr_feats = ['PAR_abs', 'RH', 'Tsfc', 'NDVI', 'BBB']
twr_hypp ={'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 750, 'subsample': 0.8}

twr_y = twr['CO2flx']
twr_X = twr[twr_feats]

# %% get data AIRBORNE
air = pd.read_csv(folder_data+'airborne_final.csv',
                 index_col=0)


air_feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Grs', 'Bld', 'SuC', 'SpC', 'Wat', 'FnB',
             'dFr', 'rivK', 'hV', 'pV', 'zeeK', 'kV', 'V', 'W', 'OWD']
air_hypp = {'learning_rate': 0.005, 'max_depth': 6, 'n_estimators': 750, 'subsample': 0.6}

air_X = air[air_feats]
air_y = air['CO2flx']

#%% get data MERGED
mer = pd.read_csv(folder_data+'merged_final.csv',
                 index_col=0)

mer_13feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'SuC', 'SpC', 'Wat', 'dFr', 'rivK', 'pV', 'zeeK', 'V', 'BBB']
mer_13hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.7}
mer_6hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}
mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']

mer_X = mer[mer_6feats]
mer_y = mer['CO2flx']
mer_hypp = mer_6hypp

#%% select data for shapley analysis

X = twr_X; y = twr_y; hyperparams = twr_hypp

X100 = shap.utils.sample(X, 100)


#%% fit optimized model

model_xgb = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
             max_depth = hyperparams['max_depth'], 
             n_estimators = hyperparams['n_estimators'],
             subsample = hyperparams['subsample']).fit(X, y)# next: with optimized parameters

#%% initialize explainer
explainer_xgb = shap.TreeExplainer(model_xgb, X100)

#%% it is possible to explain only part of the dataset, for example:

    #X = X[mer.source == 'airborne']
#X = X[(X.Tsfc > 10) & (X.Tsfc <20) ]
#X = X[(X.Tsfc > 20)]
#X = X[X.PAR_abs > 800] # this should be un-commented for linear regression at the end of the script

#%% explaining values with shapley explainer

shap_values_xgb = explainer_xgb(X) # takes ~15 minutes

#%% NOW PLOTTING

#%% shapley has many plotting options 
# here a bunch of shapley plots for inspiration

sample_ind=15

shap.plots.scatter(shap_values_xgb[:,"PAR_abs"], color=shap_values_xgb[:, 'Tsfc'])

shap.plots.bar(shap_values_xgb)

shap.plots.heatmap(shap_values_xgb[:1000])

shap.plots.beeswarm(shap_values_xgb, max_display=30)

shap.force_plot(base_value=explainer_xgb.expected_value, shap_values=shap_values_xgb.values[sample_ind,:],
                features = X.iloc[sample_ind,:].round(2), feature_names=X.columns, matplotlib=True,
                show=True, figsize=(20,3), text_rotation=0)


#%% beeswarm plot (overview)

fig, ax = plt.subplots(figsize=(15,15))
shap.plots.beeswarm(shap_values_xgb, max_display=6, show=False)
plt.title('Feature importance based on shapley values')#', PAR>100')
plt.tight_layout()
#%% save figure
#fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/merged6_beeswarm_2510.png", dpi=300)

#%% scatterplot 
# any feature from the model can filled in at 'feature=' 

fig, ax = plt.subplots(figsize=(15,15))
feature = 'PAR_abs'
shap.plots.scatter(shap_values_xgb[:,feature], show=False,
                   title= 'Shapley values of PAR_abs \n merged 6 model', 
                   color=shap_values_xgb[:,'BBB']) # again: every feature is possible for the colors
plt.xlabel(feature)
plt.ylabel('Shapley value of ' + feature)
plt.axhline(0, color='gray', ls='--')
plt.tight_layout()
#plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/merged6_Grs_bbb.png", dpi=300)


#%% make big plot: 6 plots in 1
fig, ((ax1, ax2,ax3), (ax4,ax5, ax6)) = plt.subplots(2,3,
                                                        figsize=(20,10))


### AX1
shap.plots.scatter(shap_values_xgb[:,'PAR_abs'], show=False,
                   color=shap_values_xgb[:,'Tsfc'], ax=ax1, ylabel=None)
ax1.set_ylabel('Shapley value')
ax1.set_xlabel('PAR_abs')
ax1.set_frame_on(True)
ax1.text(1600,6, 'BBB &\nPAR_abs',fontdict={'fontweight':'bold'})


### AX2
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                   color=shap_values_xgb[:,'PAR_abs'], ax=ax2)
ax2.set_ylabel('Shapley value')
ax2.set_xlabel('BBB')
ax2.text(350,5, ' BBB &\nPAR_abs', fontdict={'fontweight':'bold'})


### AX3
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                   color=shap_values_xgb[:,'Tsfc'], ax=ax3)
ax3.set_ylabel('Shapley value')
ax3.set_xlabel('BBB')
ax3.text(350,5, ' BBB\n& Tsfc', fontdict={'fontweight':'bold'})



### AX4
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                   color=shap_values_xgb[:,'RH'], ax=ax4)
ax4.set_ylabel('Shapley value')
ax4.set_xlabel('BBB')
ax4.text(350,5, ' BBB\n& RH', fontdict={'fontweight':'bold'})


### AX5
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                    color=shap_values_xgb[:,'Grs'], ax=ax5)
ax5.set_ylabel('Shapley value')
ax5.set_xlabel('BBB')
ax5.text(350,5, ' BBB\n& Grs', fontdict={'fontweight':'bold'})


### AX6
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                    color=shap_values_xgb[:,'SpC'], ax=ax6)
ax6.set_ylabel('Shapley value')
ax6.set_xlabel('BBB')
ax6.text(350,5, ' BBB\n& SpC', fontdict={'fontweight':'bold'})

fig.subplots_adjust(wspace=0.2, hspace=0.2)

fig.suptitle('Shapley analysis of BBB')
#%%
#fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/shap_BBB_scatter6_PAR_titleshor_512.png", dpi=300)


#%%  linear regression on part of BBB-range
# important: here, shapley explained for X = X[X.PAR_abs > 800] (see above)

# create mask for range of BBB
mask = (X.BBB>90) & (X.BBB < 150)

df = pd.DataFrame()

# select BBB values in X where BBB in range from mask
df['BBB'] = X[mask].BBB

# select corresponding shapley values for BBB in this range
df['shapley'] = shap_values_xgb[:,'BBB'].values[mask]

#%% fit linear regression on these values

lm_fit = smf.ols('shapley ~ BBB',data=df).fit()
#%% store coefficients and other results

b0 = lm_fit.params.Intercept.round(2)
b1 = lm_fit.params.BBB.round(3)
conf_int = lm_fit.conf_int()
r2 = lm_fit.rsquared.round(2)

#%% print results

print(lm_fit.summary())

#%% plot figure 
fig, ax = plt.subplots()
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                   title= 'Linear regression on shapley values when PAR > 800 \n for 90 < BBB < 150', 
                   color=shap_values_xgb[:,'Tsfc'], 
                   alpha=0.9, dot_size=8)

# create sequence of numbers for lin reg
xseq = np.linspace(90, 150, num=500)

# plot regression line
plt.plot(xseq, b0 + b1 * xseq, color="black", lw=2, ls='dashed')

# add text with results
plt.text(250, 2.5, "y = %s + %s * x \nR2 = %s"
         % (b0, b1, r2))


# show confidence interval
y1 = conf_int.loc['Intercept', 0] + conf_int.loc['BBB', 0] * xseq
y2 = conf_int.loc['Intercept', 1] + conf_int.loc['BBB', 1] * xseq

plt.fill_between(xseq, y1, y2, color='darkgrey', alpha=0.6)


#plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/shap_linreg_conf_int_alpha3.png", dpi=300)


