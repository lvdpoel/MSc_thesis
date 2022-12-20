"""
@author: l_vdp

This script provides two functions: get_cond and create_df.

get_cond gets the correct format for a 'condition', which can be used as a mask in selecting
rows from a dataframe and is based on a PAR or Tsfc value. For PAR, the condition is
+/- 200, for Tsfc, the condition is +/- 2.

This condition can be applied on the merged, airborne or tower dataset. If the condition
is applied, the resulting dataset has a 

create_df uses get_cond to create a dataframe, based on the condition provided
by get_cond. This dataframe

The function create_df is imported in other scripts such as sim_make_bigplot.py
and sim_overview_df,


"""
#%% import

import pandas as pd

#%% get conditions to create sub-dataframe
# PAR +/- 200 and Tsfc +/- 2

def get_cond(feat, value, data):
    """
    feat: feature 'PAR_abs' or 'Tsfc'
    value: value of feature around which range should be computed
    data: dataframe from which rows should be selected, e.g. merged dataset
    """
    value = float(value)
    
    # for PAR: range of +/- 200
    if feat == 'PAR_abs':
        upper = value + 200
        lower = value - 200
        
    # for Tsfc: range of +/- 2
    elif feat == 'Tsfc':
        upper = value + 2
        lower = value - 2
        
    cond = (data[feat] > lower) & (data[feat] < upper)
    
    if value == 0:
        cond = (data[feat] < 2)
    return cond 
        

#%% function to create dataframe, based on condition 

def create_df(PAR_value, Tsfc_value, data):
    """
    PAR_value: value for PAR around which range should be computed
    Tsfc_value: value of Tsfc around which range should be computed
    data: dataframe from which rows should be selected, e.g. merged dataset
    """
    mask = data[get_cond('PAR_abs', PAR_value, data) & get_cond('Tsfc', Tsfc_value, data)]
    
    # check if there exists data for the combination of PAR and Tsfc
    if len(mask) != 0:
        
        # create dataframe
        df = pd.DataFrame(index=range(300))    
        
        df['PAR_abs'] = PAR_value #  constant selected PAR value
        df['Tsfc'] = Tsfc_value # constant selected Tsfc value
        df['RH'] = mask['RH'].mean() # constant mean RH value, based on masked dataframe
        df['Grs'] = mask['Grs'].mean() # same as with RH
        df['SpC'] = mask['SpC'].mean() # sameas with RH
        df['BBB'] = range(300) # artifical BBB values
        df['BBB_og'] = mask['BBB'].sample(n=300, ignore_index=True, replace=True) # keep real BBB values 
    
    else:
        print('There is no data with PAR=', PAR_value,'and Tsfc=', Tsfc_value, '')
        df = pd.DataFrame()
    
    return mask, df
    
    



    
    


                         