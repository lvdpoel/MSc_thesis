# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 15:36:20 2022

@author: l_vdp
"""

#%%
import pandas as pd
import shap
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import statsmodels.api as sm # Getting acces to statistical models
import statsmodels.formula.api as smf # A convenience interface for specifying models using formula strings and DataFrames
import scipy.stats as stats


#%%
# load JS visualization code to notebook
shap.initjs()
#%% get data
#%%
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
folder_figures = 'C:/Users/l_vdp/Documents/MSc_Thesis/figures/'
#%% tower data

twr = pd.read_csv(folder_data+'tower_shuffled_3009.csv',
               index_col=0)

twr_feats = ['PAR_abs', 'RH', 'Tsfc', 'NDVI', 'BBB']
twr_hypp ={'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 750, 'subsample': 0.8}

twr_y = twr['CO2flx']
twr_X = twr[twr_feats]

# %% get data AIRBORNE
air = pd.read_csv(folder_data+'airborne_shuffled_2410.csv',
                 index_col=0)


air_feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'Grs', 'Bld', 'SuC', 'SpC', 'Wat', 'FnB',
             'dFr', 'rivK', 'hV', 'pV', 'zeeK', 'kV', 'V', 'W', 'OWD']
air_hypp = {'learning_rate': 0.005, 'max_depth': 6, 'n_estimators': 750, 'subsample': 0.6}

air_X = air[air_feats]
air_y = air['CO2flx']

#%% get data MERGED
mer = pd.read_csv(folder_data+'merged_shuffled_2410.csv',
                 index_col=0)

mer_13feats = ['PAR_abs', 'Tsfc', 'NDVI', 'RH', 'SuC', 'SpC', 'Wat', 'dFr', 'rivK', 'pV', 'zeeK', 'V', 'BBB']
mer_13hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.7}
mer_6hypp = {'learning_rate': 0.005, 'max_depth': 9, 'n_estimators': 1000, 'subsample': 0.8}
mer_6feats = ['PAR_abs', 'Tsfc', 'RH', 'Grs', 'SpC', 'BBB']

mer_X = mer[mer_6feats]
mer_y = mer['CO2flx']
#%%
peat  = pd.read_csv(folder_data+'merged_peat99.csv', index_col=0, low_memory=False)
peat_X = peat[mer_6feats]
peat_y = peat['CO2flx']

data_noBld = mer[mer.Bld<0.03]
data_noBld_X = data_noBld[mer_6feats]
data_noBld_y = data_noBld['CO2flx']
#%%
#X = data_noBld_X 
X = mer_X
X100 = shap.utils.sample(X, 100)
#y = data_noBld_y
y = mer_y
hyperparams = mer_6hypp

#%% reall stuff 

# # ### from here: real stuff!
model_xgb = XGBRegressor(learning_rate = hyperparams['learning_rate'], 
             max_depth = hyperparams['max_depth'], 
             n_estimators = hyperparams['n_estimators'],
             subsample = hyperparams['subsample']).fit(X, y)# next: with optimized parameters

#%% 
start = datetime.now()

# # # explain the XGB model 
explainer_xgb = shap.TreeExplainer(model_xgb, X100)
#%%
# als je alleen wil kijken naar specifiek gedeelte
#X = X[mer.source == 'airborne']
#X = X[(X.Tsfc > 10) & (X.Tsfc <20) ]
#X = X[(X.Tsfc > 20)]
#X = X[X.PAR_abs > 800]
#%%
shap_values_xgb = explainer_xgb(X) #eerst X # duurt 15 minuten!

end = datetime.now()

print(end-start)
 #%%
sample_ind=45
# make a standard partial dependence plot with a single SHAP value overlaid
fig,ax = shap.partial_dependence_plot(
    "BBB", model_xgb.predict, X, model_expected_value=True,
    feature_expected_value=True, show=False, ice=False,
    shap_values=shap_values_xgb[sample_ind:sample_ind+1,:]
)
#%% shapl.plots options for inspiration
sample_ind=15
shap.plots.scatter(shap_values_xgb[:,"BBB"])
shap.plots.scatter(shap_values_xgb[:,"zeeK"], color=shap_values_xgb[:, 'rivK'])
shap.plots.bar(shap_values_xgb)
shap.plots.heatmap(shap_values_xgb[:1000])
shap.plots.scatter(shap_values_xgb[:,"PAR_abs"], color=shap_values_xgb[:,"kV"])
shap.plots.bar(shap_values_xgb.abs.mean(0))
shap.plots.beeswarm(shap_values_xgb, max_display=30)
shap.force_plot(base_value=explainer_xgb.expected_value, shap_values=shap_values_xgb.values[sample_ind,:],
                features = X.iloc[sample_ind,:].round(2), feature_names=X.columns, matplotlib=True,
                show=True, figsize=(20,3), text_rotation=0)
shap.dependence_plot('BBB', shap_values_xgb, X)

# save in: C:/Users/l_vdp/Documents/MSc_Thesis/figures/shapley/
#%% beeswarm
fig, ax = plt.subplots(figsize=(15,15))
shap.plots.beeswarm(shap_values_xgb, max_display=6, show=False)
plt.title('Feature importance based on shapley values')#', PAR>100')
plt.tight_layout()
#%%
fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/merged6_beeswarm_2510.png", dpi=300)

#%% scatterplot
fig, ax = plt.subplots(figsize=(15,15))
feature = 'PAR_abs'
shap.plots.scatter(shap_values_xgb[:,feature], show=False,
                   title= 'Shapley values of Grs \n merged 6 model', 
                   color=shap_values_xgb[:,'BBB'])
plt.xlabel(feature)
plt.ylabel('Shapley value of ' + feature)
plt.axhline(0, color='gray', ls='--')
plt.tight_layout()
plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/merged6_Grs_bbb.png", dpi=300)
#%%
plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/merged6_PAR_BBB.png", dpi=300)

#%% hotness map
fig, ax = plt.subplots()
shap.plots.heatmap(shap_values_xgb[:1000], show=False)
plt.tight_layout()
#plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/airborne_211109_heatmap_noOWDGWS_noGRWT_.png", dpi=300)



#%%


#%%
plt.tight_layout()
plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/shapley/towers_shap_temp_no_apar.png", dpi=300)
#%% 6 plots in 1
fig, ((ax1, ax2,ax3), (ax4,ax5, ax6)) = plt.subplots(2,3,
                                                        figsize=(20,10))

#fig, (ax1, ax2,ax3) = plt.subplots(1,3,
 #                                                       figsize=(20,5))

### AX1
shap.plots.scatter(shap_values_xgb[:,'PAR_abs'], show=False,
                   color=shap_values_xgb[:,'Tsfc'], ax=ax1, ylabel=None)
#ax1.set_title('BBB')
ax1.set_ylabel('Shapley value')
ax1.set_xlabel('PAR_abs')
ax1.set_frame_on(True)
#ax1.text(350,3, 'PAR_abs &\Tsfc',fontdict={'fontweight':'bold'})
ax1.text(1600,6, 'BBB &\nPAR_abs',fontdict={'fontweight':'bold'})


### AX2
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                   color=shap_values_xgb[:,'PAR_abs'], ax=ax2)
#ax2.set_title('BBB & PAR_abs')
ax2.set_ylabel('Shapley value')
ax2.set_xlabel('BBB')
#ax2.text(350,3, 'BBB & \PAR_abs', fontdict={'fontweight':'bold'})
ax2.text(350,5, ' BBB &\nPAR_abs', fontdict={'fontweight':'bold'})


### AX3
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                   color=shap_values_xgb[:,'Tsfc'], ax=ax3)
#ax3.set_title('BBB & Tsfc')
ax3.set_ylabel('Shapley value')
ax3.set_xlabel('BBB')
#ax3.text(350,3, ' BBB\n& Tsfc', fontdict={'fontweight':'bold'})
ax3.text(350,5, ' BBB\n& Tsfc', fontdict={'fontweight':'bold'})

#plt.suptitle('Merged (6) model \n only explaining airborne data with  10 < Tsfc < 20')

#fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/shap_BBB_airborne_t1020.png", dpi=300)


### AX4
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                   color=shap_values_xgb[:,'RH'], ax=ax4)
#ax4.set_title('BBB & RH')
ax4.set_ylabel('Shapley value')
ax4.set_xlabel('BBB')
ax4.text(350,5, ' BBB\n& RH', fontdict={'fontweight':'bold'})


### AX5
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                    color=shap_values_xgb[:,'Grs'], ax=ax5)
#ax5.set_title('BBB & Grs')
ax5.set_ylabel('Shapley value')
ax5.set_xlabel('BBB')
ax5.text(350,5, ' BBB\n& Grs', fontdict={'fontweight':'bold'})


### AX6
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                    color=shap_values_xgb[:,'SpC'], ax=ax6)
#ax6.set_title('BBB & SpC')
ax6.set_ylabel('Shapley value')
ax6.set_xlabel('BBB')
ax6.text(350,5, ' BBB\n& SpC', fontdict={'fontweight':'bold'})

fig.subplots_adjust(wspace=0.2, hspace=0.2)

#fig.suptitle('Shapley analysis of BBB')
#%%
fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/shap_BBB_scatter6_PAR_titleshor_512.png", dpi=300)
#%%
fig, ax = plt.subplots(figsize=(7,5))
plt.scatter(X.BBB, shap_values_xgb[:,'BBB'].values, s=2, c='black')
plt.axvline(80, c='red', ls='dashed')
plt.axvline(90, c='red', ls='dashed')
plt.axvline(150, c='red', ls='dashed')

#%%
fig, ax = plt.subplots(figsize=(7,5))
plt.scatter(X.BBB, shap_values_xgb[:,'BBB'].values, s=2, c='black')
plt.xlim()
#%% KAN ALLEMAAL WEG DENK IK
# # USING NUMPY
# fig, ax = plt.subplots()

# shap.plots.scatter(shap_values_xgb[:,feature], show=False,
#                    title= 'Shapley values of PAR_abs \n merged 6 model', 
#                    color=shap_values_xgb[:,'Tsfc'])

# # Fit linear regression via least squares with numpy.polyfit
# # It returns an slope (b) and intercept (a)
# # deg=1 means linear fit (i.e. polynomial of degree 1)
# mask = (X.BBB>90) & (X.BBB < 150)
# x = X[mask].BBB
# y = pd.DataFrame(shap_values_xgb[:,'BBB'].values[mask])
# b, a = np.polyfit(x, y, deg=1)

# # Create sequence of numbers
# xseq = np.linspace(30, 240, num=500)

# # Plot regression line
# plt.plot(xseq, a + b * xseq, color="black", lw=2, ls='dashed')
# plt.text(250, 3, "y = %s + %s * x" % (a.round(2), b.round(2)))
# #%%

# fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/shap_linreg.png", dpi=300)

# #%%
# print('R2:' ,r2_score(y, y_pred))
# print('MSE:', mean_squared_error(y, y_pred))
# rss = np.sum((y - y_pred)**2)
# print('residual sum of squares is : ', rss )
# rse = np.sqrt(rss/(len(y)-2)) # estimate of standard deviation
# print('residual standard error:' ,rse )
# #%%
# se_a = rse**2 * (1/len(y) + ( ()   ) )     
# #%%
# std_est = rse **2

# #%%
# plt.scatter(X, y, s=1, c='black')
# plt.scatter(X, y_pred, s=1)
#%% SM.OLS  for 90<BBB<150 LINEAR REGRESSION

mask = (X.BBB>90) & (X.BBB < 150)

df = pd.DataFrame()
df['BBB'] = X[mask].BBB
df['shapley'] = shap_values_xgb[:,'BBB'].values[mask]

#%%
lm_fit = smf.ols('shapley ~ BBB',data=df).fit()
#%%
b0 = lm_fit.params.Intercept.round(2)
b1 = lm_fit.params.BBB.round(3)
conf_int = lm_fit.conf_int()
r2 = lm_fit.rsquared.round(2)
p_val = float(0.000)
#%%

print(lm_fit.summary())

"""
The t-statistic on the intercept is -21,72 with a p-value of 0, indicating that the intercept is significantly different than 0.
The t-statistic on the slope is 22,147, with a p-value of 0, indicating that the slope is significantly different from 0,
which means that there is a substantial association between predictor (BBB) and response (shapley value).
R2=0.49

"""
#%%
fig, ax = plt.subplots()
shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                   title= 'Linear regression on shapley values when PAR > 800 \n for 90 < BBB < 150', 
                   color=shap_values_xgb[:,'Tsfc'], 
                   alpha=0.9, dot_size=8)
# Create sequence of numbers
xseq = np.linspace(90, 150, num=500)

# Plot regression line
plt.plot(xseq, b0 + b1 * xseq, color="black", lw=2, ls='dashed')
plt.text(250, 2.5, "y = %s + %s * x \nR2 = %s"# \nP = %.3f" 
         % (b0, b1, r2))#, p_val))

# plot vertical lines
#plt.axvline(90)
#plt.axvline(150)

y1 = conf_int.loc['Intercept', 0] + conf_int.loc['BBB', 0] * xseq
y2 = conf_int.loc['Intercept', 1] + conf_int.loc['BBB', 1] * xseq
#plt.plot(xseq,y1,color='black', lw=1, ls='dotted')
#plt.plot(xseq,y2,color='black', lw=1, ls='dotted')

plt.fill_between(xseq, y1, y2, color='darkgrey', alpha=0.6)


#plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/shap_linreg_conf_int_alpha3.png", dpi=300)
    #%%
#%%
plt.plot(xseq, conf_int.loc['Intercept', 0] + conf_int.loc['BBB', 0] * xseq, 
         color="grey", lw=1, ls='solid')
plt.plot(xseq, conf_int.loc['Intercept', 1] + conf_int.loc['BBB', 1] * xseq, 
         color="grey", lw=1, ls='solid')
#%% POLYFIT
import numpy.polynomial.polynomial as poly

shap.plots.scatter(shap_values_xgb[:,'BBB'], show=False,
                   title= '10th order polynomial on shapley values when PAR>800', 
                   color=shap_values_xgb[:,'Tsfc'], 
                   alpha=0.9, dot_size=8)

coefs = poly.polyfit(X.BBB, shap_values_xgb[:,'BBB'].values, 11)
ffit = poly.polyval(X.BBB, coefs)

plt.scatter(X.BBB, ffit, s=1, c='black', label=i)

#plt.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/loll.png", dpi=300)

# Create sequence of numbers
#%%