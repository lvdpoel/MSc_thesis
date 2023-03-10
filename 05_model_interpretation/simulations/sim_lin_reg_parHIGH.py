"""
@author: l_vdp

This script performs linear regression on simulations when PAR>800 and Tsfc = 15 and 20
for BBB 90-270 and produces a plot visualising this. 

Input: dataframe with all simulated values (created in sim_overview_df.py)
Output: linear regression plot for PAR>800.
"""

#%% some imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf # A convenience interface for specifying models using formula strings and DataFrames
import numpy as np
from matplotlib.lines import Line2D

#%% get simulated data

df = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/simulations/df_all_simulated_CO2_300.csv", 
            index_col=0)
#%%

Tsfc_values = {'T0': 0, 'T5':5 , 'T10':10, 'T15': 15, 'T20':20, 'T25': 25}
colors = sns.color_palette("Paired")

#%% plot high PAR combinations to see on which range the linear regression should be run

# PAR 1200
plt.scatter(df.index, df.PAR1200_T15, s=2, 
            color = colors[list(Tsfc_values.values()).index(15)],
            marker = '.')
plt.scatter(df.index, df.PAR1200_T20, s=2,
            color = colors[list(Tsfc_values.values()).index(20)],
            marker = '.')
# PAR1600
plt.scatter(df.index, df.PAR1600_T15, s=2, 
            color = colors[list(Tsfc_values.values()).index(15)],
            marker = '^')
plt.scatter(df.index, df.PAR1600_T20, s=2, 
            color = colors[list(Tsfc_values.values()).index(20)],
            marker = '^')

# plot vertical lines to see if the estimated range is correct
plt.axvline(90)
plt.axvline(230)

#%% set up range for linear regression

lwr = 90
upr = 270

#%% select values within the range for linear regression and put together in one dataframe

PAR1200T15 = df[(df.index<upr) & (df.index>lwr)]['PAR1200_T15'].to_frame(name='co2')
PAR1200T20 = df[(df.index<upr) & (df.index>lwr)]['PAR1200_T20'].to_frame(name='co2')
PAR1600T15 = df[(df.index<upr) & (df.index>lwr)]['PAR1600_T15'].to_frame(name='co2')
PAR1600T20 = df[(df.index<upr) & (df.index>lwr)]['PAR1600_T20'].to_frame(name='co2')

df_long = pd.concat([PAR1200T15, PAR1200T20, PAR1600T15, PAR1600T20])
df_long['BBB'] =df_long.index

#%% plot all these points

plt.scatter(df_long.index, df_long.co2, s=1)

#%% linera regression on these points and store results
lm_fit = smf.ols('co2 ~ BBB',data=df_long).fit()
b0 = lm_fit.params.Intercept.round(2)
b1 = lm_fit.params.BBB.round(3)
conf_int = lm_fit.conf_int()
r2 = lm_fit.rsquared.round(2)

#%% print results
print(lm_fit.summary())

#%% plot figure 

fig, ax = plt.subplots(figsize=(6,4))

plt.scatter(df.index, df.PAR1200_T15, s=2, 
            color = colors[list(Tsfc_values.values()).index(15)],
            marker = '.')
plt.scatter(df.index, df.PAR1200_T20, s=2,
            color = colors[list(Tsfc_values.values()).index(20)],
            marker = '.')
# PAR1600
plt.scatter(df.index, df.PAR1600_T15, s=2, 
            color = colors[list(Tsfc_values.values()).index(15)],
            marker = '^')
plt.scatter(df.index, df.PAR1600_T20, s=2, 
            color = colors[list(Tsfc_values.values()).index(20)],
            marker = '^')

# Create sequence of numbers
xseq = np.linspace(lwr, upr, num=500)

# Plot regression line
plt.plot(xseq, b0 + b1 * xseq, color="black", lw=1, ls='dashed')
plt.text(110, -11, "y = %s + %s * x \nR2 = %s "
         % (b0, b1, r2))

# confidence interval
y1 = conf_int.loc['Intercept', 0] + conf_int.loc['BBB', 0] * xseq
y2 = conf_int.loc['Intercept', 1] + conf_int.loc['BBB', 1] * xseq

plt.fill_between(xseq, y1, y2, color='grey', alpha=0.3)

legend_elements = [Line2D([0], [0], marker = 'o', label='Tsfc =  15', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T15')]),
                  Line2D([0], [0],  marker ='o',label='Tsfc = 20', color='white', markersize=15, markerfacecolor = colors[list(Tsfc_values).index('T20')]),
                  Line2D([0], [0], marker ='.', label='PAR_abs = 1200', color='white', markersize=10, markerfacecolor = 'black'),#colors[list(PAR_values).index('PAR1200')]),
                  Line2D([0], [0], marker ='^',label='PAR_abs = 1600', color='white', markersize=10, markerfacecolor = 'black')
                  ]
plt.legend(handles=legend_elements, loc='lower right')


plt.title('Linear regression on simulations for PAR > 800 \n for 90 < BBB < 270')
plt.ylabel('Predicted CO2 [umol m-2 s1]')
plt.xlabel('BBB [mm]')
#%% save figure 
#fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/simulationsPARHIGH_linreg.png", dpi=300)
