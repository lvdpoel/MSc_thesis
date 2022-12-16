# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 11:28:45 2022

@author: l_vdp
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
from matplotlib import dates as mdates
#%%
df = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/BBB_locas.csv",
                 index_col=0)

df_zv_lw = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/OWASIS_zv_lw.csv",
                index_col=0)

df_20 = pd.read_csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/OWASIS_20locas.csv",
                 index_col=0)
#%%
df=df_zv_lw
df['datetime'] = None
for i in df.index:
    df.loc[i, 'datetime'] = datetime.strptime(str(i), '%Y%j')

#%%
fig, ax = plt.subplots()
for col in ['BBB_lw3', 'BBB_lw4', 'BBB_lw5', 'BBB_lw6',
       'BBB_lw7']:#df.columns[:-1]:
    plt.plot(df.datetime, df[col], linewidth=1, label=str(int(col[-1])-2))
    
plt.legend()
plt.xticks(rotation=45)
plt.title('BBB, increasing number more eastward \n same lat as lw')
plt.ylabel('BBB [mm]')
#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/BBB_over_time.png', bbox_inches='tight', dpi=300)
()
#%%
fig, ax = plt.subplots()
plt.plot(df.datetime, df.BBB_zv, label='Zegveld')
plt.plot(df.datetime, df.BBB_lw, label='Langeweide')
for col in ['BBB_1',  
            'BBB_lw3', 
            'BBB_lw4', 
            'BBB_lw5',
            'BBB_lw6',
            'BBB_lw7'
            ]:#df.columns[:-1]:
    plt.plot(df.datetime, df[col], linewidth=1)
plt.legend(loc='best')
plt.xticks(rotation=45)
plt.title('BBB over time')
plt.ylabel('BBB [mm]')


# Set X range. Using left and right variables makes it easy to change the range.
#
left = date(2020, 2, 1)
right = date(2022, 1, 31)
# Format the date into months & days
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y')) 

# Change the tick interval
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3)) 

# Puts x-axis labels on an angle
plt.gca().xaxis.set_tick_params(rotation = 30)  

# Changes x-axis range
plt.gca().set_xbound(left, right)

#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/BBB_over_meas_time_lwzv_all_2.png', bbox_inches='tight', dpi=300)
()
#%%
fig, ax = plt.subplots()

ax.plot(df.datetime, df.BBB_lw, label = 'BBB')
ax.set_ylabel('BBB [mm]')
ax.legend()

ax = ax.twinx()
ax.plot(df.datetime, df.GWS_lw, color='black', label='GWS')
ax.set_ylabel('GWS [mNAP]')

#%%


# Set X range. Using left and right variables makes it easy to change the range.
#
left = date(2020, 2, 1)
right = date(2022, 1, 31)

# Format the date into months & days
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y')) 

# Change the tick interval
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3)) 

# Puts x-axis labels on an angle
plt.gca().xaxis.set_tick_params(rotation = 30)  

# Changes x-axis range
plt.gca().set_xbound(left, right)

ax.legend()
#%%
plt.scatter(x=df_zv_lw['BBB_zv'], y=df_zv_lw['GWS_zv'], c=df_zv_lw['OWD_zv'], s=3)
plt.colorbar(label='OWD [m -mv]')
plt.xlabel('BBB [mm]')
plt.ylabel('GWS [mNAP]')
plt.title('OWASIS variables Zegveld')
plt.axvline(100)
plt.axvline(120)
plt.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/owasis_zv_owd.png', bbox_inches='tight', dpi=300)
#%%
BBB_cols = []
for col in df.columns:
    if 'BBB' in col:
        BBB_cols.append(col)
        
        
#%% 20 random locations and zv and lw

df=df_20
for col in BBB_cols:
    plt.plot(df['datetime'], df[col], c='black', lw=0.3)
plt.plot(df_zv_lw.datetime, df_zv_lw['BBB_zv'], label='Zegveld', lw=2)
plt.plot(df_zv_lw.datetime, df_zv_lw['BBB_lw'], label='Langeweide', lw=2)
plt.legend()
plt.title('BBB over time')
plt.ylabel('BBB [mm]')


# Set X range. Using left and right variables makes it easy to change the range.
#
left = date(2020, 2, 1)
right = date(2022, 1, 31)

# Format the date into months & days
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y')) 

# Change the tick interval
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3)) 

# Puts x-axis labels on an angle
plt.gca().xaxis.set_tick_params(rotation = 30)  

# Changes x-axis range
plt.gca().set_xbound(left, right)

#%%
fig.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/BBB_over_time_20.png', bbox_inches='tight', dpi=300)

#%%
col = 'BBB_18'
plt.plot(df.datetime, df[col])
