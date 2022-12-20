# -*- coding: utf-8 -*-
"""
@author: l_vdp

This script creates a Datetime column in the merged dataset with the correct datetime format,
because the datetime formats from tower and airborne data differed.

Input: merged dataset without correct datetime format
Output: merged dataset with correct datetime format
"""

#%% some imports

import pandas as pd
from datetime import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%% read data
 
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
df = pd.read_csv(folder_data+'merged_shuffled_2410.csv',
                 index_col=0, na_values='nan')


#%% 

df['Datetime'] = None
for i in df.index:
    dt_twr = df.loc[i,'datetime']
    dt_air = df.loc[i, 'Date']
    if dt_twr is not np.nan:
        df.loc[i, 'Datetime'] = datetime.strptime(dt_twr, '%Y-%m-%d %H:%M:%S')
    else:
        df.loc[i, 'Datetime'] = datetime.strptime(dt_air, ' %Y-%m-%d')
        
        
    
#%% save new dataframe
#df.to_csv(folder_data+'merged_shuffled_2410.csv')

#%% scatter plot CO2 per datatype

sns.scatterplot(df.Datetime, df.CO2flx, hue=df.source)
#plt.savefigure("C:/Users/l_vdp/Documents/MSc_Thesis/figures/scatterco2.png")
    