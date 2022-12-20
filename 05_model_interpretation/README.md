# Model interpretation

In the ```shap_analysis``` script, the SHAP package is used to calculate shapley values of feautures in the best performing model (merged 6).
Overview plots are made, and linear regression is run on shapley values explaining PAR>800.

In the folder ```simulations```, the simulation scripts are stored.

There are two ways in which simulation plots were made. Both use the function ```create_df``` in ```prepare_data_for_simulations```. This function creates a dataframe based on a PAR and Tsfc value. It takes the mean of the rest of the variables, and ranges BBB from 0 to 300.

In the first way of simulations, in ```sim_make_bigplot```, the ```create_df``` function is called for every subplot separately, creating one big figure. Combinations of PAR and Tsfc values are set up manually. 

In the second way of simulations, in ```sim_create_overview_df```, the ```create_df``` function is called for every possible combination of PAR and Tsfc. A dataframe is created with predictions for every PAR-Tsfc combination. 

In the scripts that start with ```sim_lin_reg_```, this overview dataframe is used to plot the simulated values. In both scripts, linear regression is run on a range of BBB values. 

