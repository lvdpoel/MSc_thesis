# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:44:49 2022

@author: l_vdp
"""

import pandas as pd
from datetime import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#%%

folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
df = pd.read_csv(folder_data+'merged_shuffled_2410.csv',
                 index_col=0, na_values='nan')


#%%

df['Datetime'] = None
counter = 0 
twr = 0
air = 0
for i in df.index:
    dt_twr = df.loc[i,'datetime']
    dt_air = df.loc[i, 'Date']
    if dt_twr is not np.nan:
        twr +=1
        df.loc[i, 'Datetime'] = datetime.strptime(dt_twr, '%Y-%m-%d %H:%M:%S')
    else:
        df.loc[i, 'Datetime'] = datetime.strptime(dt_air, ' %Y-%m-%d')
        
        
        
print(counter)
    
#%%
#%%
#df.to_csv(folder_data+'merged_shuffled_2410.csv')

sns.scatterplot(df.Datetime, df.CO2flx, hue=df.source)
plt.savefigure("C:/Users/l_vdp/Documents/MSc_Thesis/figures/scatterco2.png")
    
#%%
fig, ax = plt.subplots()
maskdf = df[df.source == 'tower']
sns.scatterplot(maskdf.Datetime, maskdf.CO2flx, hue=maskdf.BBB, s=10)
plt.title('Tower data')
plt.xticks(rotation=45)
#%%
fig.savefig("C:/Users/l_vdp/Documents/MSc_Thesis/figures/tower_co2_bbb.png", dpi=300, bbox_inches='tight', )
