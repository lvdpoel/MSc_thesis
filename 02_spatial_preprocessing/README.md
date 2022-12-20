# Spatial preprocessing

Here, I describe the scripts and their functions, in the order they should be understood. 

### 1. Scripts in ```preparation```. 

The script ```read_modis``` joins all downloaded modis files into one .tiff file: NDVI_all.tiff

In ```reclassify_soil``` the soil classes are reclassified

### 2. Scripts in ```functions```

In this folder, all scripts are functions that are used by scripts in ```02_spatial_preprocessing```. 

Every script that starts with ```find``` finds the correct, i.e. closest in time, NDVI or OWASIS file for the airborne footprint or tower measurement. 

Every script that starts with ```calc``` means: calculate value for XXX in the airborne footprint, where XXX can be ```ruimt_data``` : soil and land use maps; ```spat_temp_data```: spatial temporal data, OWASIS variables, or ```ndvi```: NDVI.

```importMaps``` is a function to read the soil and land use class maps that were provided by Water Systems & Global Change. 

```twr_area``` uses the location of the tower to create a raster of the area around the tower, which can later be used for spatial analysis.

### 3. Scripts in current repository

These scripts use the functions in ```functions``` to calculate the feature values in the footprints. There are two types: airborne footprints overlaid with spatial data (starting with ```fp_```) and tower footprints overlaid with spatial data (starting with ```get_tower_```).

- ```fp_ruimtdata_analysis_final``` computes the presence (%) of soil and land use classes in the airborne footprints
- ```fp_spat_temp_analysis_final``` computes the average value of OWASIS variables and NDVI in the airborne footprints
- ```get_tower_ndvi```computes the average NDVI value in an area around the tower, using the correct (closest in time) NDVI file
- ```get_tower_owasis``` computes the average OWASIS variables in an area around the tower,  using the correct (closest in time) OWASIS files
- ```get_tower_spatialinfo_fun``` computes the percentage of every land and soil class in the average accumulated footprint around the tower (1 value for all measurements)
- ```analyse_BBB``` computes the values of OWASIS variables for every date the data was available, in 20 locations from the airborne dataset.

### 4. Scripts in ```clean_datasets```

These scripts should be used after the spatial preprocessing done by the scripts described above. 

```clean_tower_data``` and ```clean_airborne_data``` are used to clean the respective datasets. 

```merge_airborne_tower``` merges the two datasets, taking into account previous differences.

```set_datetimes_merged``` ensures there is a column with datetime in the correct format.




