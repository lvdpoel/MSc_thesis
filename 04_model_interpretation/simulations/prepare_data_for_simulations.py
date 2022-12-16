# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:22:11 2022

@author: l_vdp
"""

import pandas as pd
import matplotlib.pyplot as plt

#%%
folder_data = "C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/"
# #%%
# twr  = pd.read_csv(folder_data+'tower_shuffled_3009.csv',
#                index_col=0)
# air = pd.read_csv(folder_data+'airborne_shuffled_2410.csv',
#                  index_col=0)
mer = pd.read_csv(folder_data+'merged_shuffled_2410.csv',
                index_col=0)
# #%%
# cond_par0 = (mer['PAR_abs'] < 0.5)
# cond_par500 = (mer['PAR_abs'] > 490) & (mer['PAR_abs'] < 510)
# cond_par1250 = (mer['PAR_abs'] > 1240) & (mer['PAR_abs'] < 1260)

# cond_t5 =  (mer['Tsfc'] < 6) & (mer['Tsfc'] > 4)
# cond_


#%%
def get_cond(feat,value, data):
   
    if value == 0:
        cond = (data[feat] < 2)
    else:
        value = float(value)
        upper = value + 0.2 * value
        lower = value - 0.2 *  value
        cond = (data[feat] > lower) & (data[feat] < upper)
    return cond
#%%
def get_cond(feat, value, data):
    value = float(value)
    if feat == 'PAR_abs':
        upper = value + 200
        lower = value - 200
    elif feat == 'Tsfc':
        upper = value + 2
        lower = value - 2
    cond = (data[feat] > lower) & (data[feat] < upper)
    if value == 0:
        cond = (data[feat] < 2)
    return cond 
        
        

#%%

# par0t5 = mer[(mer['PAR_abs']<0.5) & get_cond('Tsfc', 5)]
# par0t5rh = par0t5['RH'].mean()
# par0t5_df = pd.DataFrame(index=range(200))
# par0t5_df['PAR_abs']=0
# par0t5_df['Tsfc'] = 5
# par0t5_df['RH'] = par0t5['RH'].mean()
# par0t5_df['Grs'] = par0t5['Grs'].mean()
# par0t5_df['SpC'] = par0t5['SpC'].mean()
# par0t5_df['BBB'] = range(200)
# par0t5_df['BBB_original'] = par0t5['BBB'].sample(n=200, ignore_index=True)

#%%
#%%
def create_df(PAR_value, Tsfc_value, data):
    mask = data[get_cond('PAR_abs', PAR_value, data) & get_cond('Tsfc', Tsfc_value, data)]
    #print(len(mask))
    # nbins=10
    # plt.hist(mask.BBB, alpha=0.5,bins=nbins, label=Tsfc_value, density=True,
    #           color = colors[list(Tsfc_values.values()).index(Tsfc_value)])
    # plt.legend(title='Tsfc')
    # plt.title('Histograms of BBB when PAR = 1600')
    # plt.xlabel('BBB')
    # plt.ylabel('Density')
    if len(mask) != 0:
        df = pd.DataFrame(index=range(300))
        df['PAR_abs'] = PAR_value
        df['Tsfc'] = Tsfc_value
        #df['PAR_abs'] = mask['PAR_abs'].sample(n=200, ignore_index=True, replace=True)
        #df['Tsfc'] = mask['Tsfc'].sample(n=200, ignore_index=True, replace=True)
        df['RH'] = mask['RH'].mean()
        df['Grs'] = mask['Grs'].mean()
        df['SpC'] = mask['SpC'].mean()
        df['BBB'] = range(300)
        df['BBB_og'] = mask['BBB'].sample(n=300, ignore_index=True, replace=True)
    
    else:
        print('There is no data with PAR=', PAR_value,'and Tsfc=', Tsfc_value, '')
        df = pd.DataFrame()
    
    return mask, df
    
    

#%%
#create_df(PAR_value = 800, Tsfc_value = 0, data=mer)
#create_df(PAR_value = 800, Tsfc_value = 5, data=mer)
create_df(PAR_value = 1200, Tsfc_value = 10, data=mer)
create_df(PAR_value = 1200, Tsfc_value = 15, data=mer)
create_df(PAR_value = 1200, Tsfc_value = 20, data=mer)
create_df(PAR_value = 1200, Tsfc_value = 25, data=mer)

plt.savefig('C:/Users/l_vdp/Documents/MSc_Thesis/figures/bbb_par1200_Tsfc152025.png', bbox_inches='tight', dpi=300)

#%%


    
    


                         