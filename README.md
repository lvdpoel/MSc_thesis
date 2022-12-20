# MSc_thesis

In this directory I present the scripts used for my Master Thesis: **Analysing airborne CO2 flux measurements in relation to landscape characteristics with machine learning** 

Master Thesis Water Systems and Global Change Group in partial fulfillment of the degree of Master of Science in Climate Studies at Wageningen University, the Netherlands. The scripts are organized in folders which are ordered in the same way as the thesis. 

Supervisors: dr. R.W.A. Hutjes, dr. B. Kruijt

Examiner: dr. S. Paparrizos

## Scripts

The folders contain all necessary scripts to carry out the research. 
In every folder, there is a README.md file where I explain what is done in which script. Below, I present an overview of tasks per folder.

**Overview**
- 01_footprint_modelling: the footprint model by Kljun et al. (2015) is used to calculate the footprints for every airborne measurment.
- 02_spatial_preprocessing: the modelled airborne footprints and calculated tower footprints are overlaid with spatial data from maps, remote sensing NDVI, and daily water information product OWASIS. This results in three final datasets: tower, airborne and merged.
- 03_model_optimization: for all three obtained datasets, feature selection and hyperparameter tuning are performed as model optimization steps.
- 04_model_evaluation: the optimized models are evaluated.
- 05_model_interpretation: the models are interepreted by shapley value analysis and simulations.


## Abstract 
Drained fen meadows in the Netherlands are a substantial source of carbon dioxide and further understanding of its
drivers is necessary. Taking eddy covariance (EC) carbon dioxide (CO2) flux measurements from ultra-light aircrafts
has been developed as a new approach to cover more spatial heterogeneity in and between footprints than with
conventional EC towers. The current study aims to find a relationship between landscape characteristics and CO2
fluxes by combining airborne and tower CO2 data with spatial information from maps, remote sensing NDVI, and a
daily soil-water information product. The data is given as input to a boosted regression tree (BRT) algorithm. Feature
selection and hyperparameter tuning were applied as model optimization techniques, resulting in an optimized model
with R2 = 0.61. No significant relationship with land use and soil classes was found, but a consistent influence of
water storage capacity [mm] was apparent in two cases: with PAR = 0 and PAR > 800 (PAR: photosynthetically active
radiation). The results indicate that, in these two cases, every extra mm of water storage capacity leads to emissions
of 370 kg CO2 per hectare per year. This converts to emissions of 3.7 tonnes CO2 ha-1 yr-1 per 10 centimeters reduced
efficient water table depth, which corresponds closely to current estimates. We conclude the method is promising
and its potential can be fully utilized when multi-year temporally continuous data is available.


## References
Kljun, N., Calanca, P., Rotach, M. W., & Schmid, H. P. (2015). The simple two-dimensional parameterisation for Flux Footprint Predictions FFP. Geoscientific Model Development Discussions, 8(8).
