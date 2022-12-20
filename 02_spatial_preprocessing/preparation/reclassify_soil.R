"""
This script is used to reclassify the soil map. See thesis 
for more explanation.

"""

rm(list=ls())

# libs
library(terra)
library(foreign)
library(sf)
library(dplyr)


sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

# get soil data and rename columns in classes
path <- "~/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden"
Bodempath <- paste0(path, '/Bodemkaart')
dataMaps <- rast(paste0(Bodempath , '/Bodemkaart_25m.tif'))
map <- rast(paste0(Bodempath , '/Bodemkaart_25m.tif'))
classes <- read.dbf(paste0(Bodempath , '/Bodemkaart_5m.tif.vat.dbf'), as.is = FALSE)
names(classes)[names(classes) == 'Value'] <- 'ID'
names(classes)[names(classes) == 'main__mp_s'] <- 'class'


# get official names of soil codes and classes from BRO
bropath <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden/Bodemkaart/BRObodemkaart.gpkg"
st_layers(bropath)
soilunits <- st_read(bropath, layer='mp_soil_units')
soildf <- as.data.frame(soilunits)  

# create empty columns for new code and class
soildf['newcode'] <- NaN
soildf['newclass'] <- NaN

# for every soil code: reclassify 
for(i in 1:length(soildf$code)){
  
  code = soildf$code[i]
  class = soildf$main_soil_classification[i]
  
  # 8 archetypes based on code
  if(code == 'Vz'){newcode = code; newclass= 'Vlierveengronden, ondergrond zand zonder humuspodzol'}
  else if(nchar(code)==2 & substr(code, 1,1) == 'V'){newcode = 'V'; newclass='Vlierveengronden'}
  else if(code == 'hVz'){newcode = code; newclass='Koopveengronden, ondergrond zand'}
  else if(nchar(code)==3 & substr(code, 1,2) == 'hV'){newcode = 'hV'; newclass='Koopveengronden'}
  else if(code == 'kVz'){newcode=code; newclass='Waardveengronden, ondergrond zand'}
  else if(nchar(code)==3 & substr(code, 1,2) == 'kV'){newcode = 'kV'; newclass= 'Waardveengronden'}
  else if(code == 'aVz'){newcode=code; newclass='Madeveengronden, ondergrond zand zonder humuspodzol'}
  else if(nchar(code)==3 & substr(code, 1,2) == 'pV'){newcode = 'pV'; newclass= 'Weideveengronden'}
  else if(nchar(code)==3 & substr(code, 2,2) == 'W' || nchar(code)==2 & substr(code,1,1)=='W' ||
          class == 'Dikke eerdgronden'){newcode='W'; newclass='Moerige gronden'}
  
  # rest of classes based on main class 
  else if(class=='Veengronden'){newcode='overigV' ;newclass='Overige veengronden'}
  else if(class == 'Podzolgronden' || class == 'Kalkloze zandgronden' || class == 'Kalkhoudende zandgronden' ||
          class == 'Niet-gerijpte minerale gronden'){newcode='zandG' ; newclass='Zandgronden'}
  else if(class == 'Zeekleigronden' || class == 'Zeer oude mariene afzettingen'){newcode = 'zeeK'; newclass='Zeeklei'}
  else if(class == 'Rivierkleigronden'|| class== 'Oude rivierkleigronden' || 
          class == 'Zeer oude fluviatiele afzettingen' || class=='Keileemgronden'){newcode='rivK'; newclass='Rivierklei'}
  else if(class == 'Leemgronden' || class=='Brikgronden' || class == 'Kalksteen verweringsgronden'){
    newcode = 'leem'; newclass='Leem en brikgronden'}
  else if(class == 'Gedefinieerde associaties'){newcode='gedA'; newclass='Gedefinieerde associaties'}
  else {newcode = NaN; newclass = NaN}
  
  # store new codeand class in soildf
  soildf$newcode[i] <- newcode
  soildf$newclass[i] <- newclass
  
}

# store new soil classes in classes (which 'belong' to our map) based on soildf
classes['newclass'] <- NaN
classes['newcode'] <- NaN

for(i in 1:length(classes$class)){
  cl <- as.character(classes$class[i])
  classes$newclass[i] <- soildf[soildf$soil_classification == cl, 'newclass']
  classes$newcode[i] <- soildf[soildf$soil_classification == cl, 'newcode']
}



write.csv(classes, "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden/Bodemkaart/reclassified_soilclasses3.csv")
