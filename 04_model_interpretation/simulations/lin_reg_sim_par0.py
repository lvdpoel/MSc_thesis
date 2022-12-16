# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 11:18:43 2022

@author: l_vdp
"""

import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error
import statsmodels.api as sm # Getting acces to statistical models
import statsmodels.formula.api as smf # A convenience interface for specifying models using formula strings and DataFrames
import scipy.stats as stats

#%%
df = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/simulations/df_all_simulated_CO2.csv", 
            index_col=0)
#%%


PAR_values = {'PAR0': 0,'PAR400' : 400, 'PAR800': 800, 'PAR1200' : 1200, 'PAR1600' : 1600}
Tsfc_values = {'T0': 0, 'T5':5 , 'T10':10, 'T15': 15, 'T20':20, 'T25': 25}

#%%

plt.scatter(df.index, df.PAR0T0, s=2, 
            color = colors[list(Tsfc_values.values()).index(0)])
plt.scatter(df.index, df.PAR0T5, s=2,
            color = colors[list(Tsfc_values.values()).index(5)])
plt.scatter(df.index, df.PAR0T10, s=2, 
            color = colors[list(Tsfc_values.values()).index(10)])
plt.axvline(150)

#%%
T0 = df[df.index<150]['PAR0T0'].to_frame(name='co2')
T5 = df[df.index<150]['PAR0T5'].to_frame(name='co2')
T10 = df[df.index<150]['PAR0T10'].to_frame(name='co2')


#%%
df_long = pd.concat([T0, T5, T10])
df_long['BBB'] =df_long.index
#%%
plt.scatter(df_long.index, df_long.co2, s=1)
#%%
lm_fit = smf.ols('co2 ~ BBB',data=df_long).fit()
#%%
b0 = lm_fit.params.Intercept.round(2)
b1 = lm_fit.params.BBB.round(3)
conf_int = lm_fit.conf_int()
r2 = lm_fit.rsquared.round(2)
p_val = float(0.000)
#%%
print(lm_fit.summary())
#%%

fig, ax = plt.subplots()

plt.scatter(df.index, df.PAR0T0, s=2, 
            color = colors[list(Tsfc_values.values()).index(0)])
plt.scatter(df.index, df.PAR0T5, s=2,
            color = colors[list(Tsfc_values.values()).index(5)])
plt.scatter(df.index, df.PAR0T10, s=2, 
            color = colors[list(Tsfc_values.values()).index(10)])

# Create sequence of numbers
xseq = np.linspace(0, 150, num=500)

# Plot regression line
plt.plot(xseq, b0 + b1 * xseq, color="black", lw=1, ls='dashed')
plt.text(120, 2.5, "y = %s + %s * x \nR2 = %s "#\nP = %.3f" 
         % (b0, b1, r2))#, p_val))

# plot vertical lines
#plt.axvline(150)

y1 = conf_int.loc['Intercept', 0] + conf_int.loc['BBB', 0] * xseq
y2 = conf_int.loc['Intercept', 1] + conf_int.loc['BBB', 1] * xseq

plt.fill_between(xseq, y1, y2, color='grey', alpha=0.3)

legend_elements = [Line2D([0], [0], marker = 'o', label='Tsfc =  0', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T0')]),
                  Line2D([0], [0],  marker ='o',label='Tsfc = 5', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T5')]),
                   Line2D([0], [0], marker = 'o', label='Tsfc = 10', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T10')]),
                  ]
                   

# Create the figure
plt.legend(handles=legend_elements, loc='upper left')#, bbox_to_anchor=(1,0.8))

plt.title('Simulations for PAR = 0')
plt.ylabel('Predicted CO2 [umol m-2 s1]')
plt.xlabel('BBB [mm]')
#%%
fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulationsPAR0_linreg.png", dpi=300)
    #%%
