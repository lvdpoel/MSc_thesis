# Footprint modelling

The ```prepare_grhart_file``` is used to make the airborne measurements file ready for the Kljun functions. Some columns are renamed, and some columns with new variables are created.

The folder ```functions_kljun``` contains the functions from Kljun et al. (2015).
These functions are called in the ```ffp_analysis``` script. There, the Kljun functions are used to calculate the footprint for every airborne measurement.
```ffp_analysis``` produces a .nc file for every footprint. 

