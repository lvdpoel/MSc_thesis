rm(list=ls())


library(terra)
library(foreign)
library(sf)
library(dplyr)


sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

path <- "~/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden"
Bodempath <- paste0(path, '/Bodemkaart')
dataMaps <- rast(paste0(Bodempath , '/Bodemkaart_25m.tif'))
map <- rast(paste0(Bodempath , '/Bodemkaart_25m.tif'))
plot(map)
classes <- read.dbf(paste0(Bodempath , '/Bodemkaart_5m.tif.vat.dbf'), as.is = FALSE)
names(classes)[names(classes) == 'Value'] <- 'ID'
names(classes)[names(classes) == 'main__mp_s'] <- 'class'

fp.folder <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_values_rasters_1-1000/"
fp.files <- list.files(fp.folder, pattern= '.nc')
fp <- rast(paste0(fp.folder, fp.files[[1]]))

fp <- project(fp, crs(dataMaps)) # duurt 4 sec
fp[is.na(fp)] <- 0
fp[fp<0] <- 0

map <- crop(dataMaps, fp, snap='out')
levels(map) <- classes$class

plot(map, type='classes', levels=classes$class, legend=TRUE, main ='Bodemkaart all classes')
values(map)


length(classes$class)# == soildf$main_soil_classification
length(soildf$soil_classification)

i=100


classes$mainclass

bropath <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden/Bodemkaart/BRObodemkaart.gpkg"

st_layers(bropath)
# 
# soiltop <-st_read(bropath, layer='soil_characteristics_top')
# map_area <- st_read(bropath, layer='map_area')
# map_area.1 <- vect(map_area)
# map_area.2 <- crop(map_area.1, x)
# #st_read(bropath, layer='soil_map')
# #soil_area <- st_read(bropath, layer='soil_area')
# st_read(bropath, layer='area_of_pedological_interest')
# sasu <- st_read(bropath, 'soil_area_soil_units') # contains map_area_id and soil_unit_code and soil_unit_seq_id
# 
# st_read(bropath, 'nga_properties')
# 
# plot(map_area.2, las=1)  
soilunits <- st_read(bropath, layer='mp_soil_units')
soildf <- as.data.frame(soilunits)  
colnames(soildf)
soildf$soil_classification



# 
# mainclasses <- soilunits$main_soil_classification
# length(mainclasses)
# values(map_area.1) <- mainclasses
# plot(map_area.1)
# plot(map_area.2, las=1, legend=T)
# 
# map_area.2$mainclasses <- mainclasses
# plot(map_area.2, las=1)# <- mainclasses
# 
# soiltop$
i=1


classes['mainclass'] <- NaN
classes['code'] <- NaN
for(i in 1:length(classes$class)){
  cl <- as.character(classes$class[i])
  classes$mainclass[i] <- soildf[soildf$soil_classification == cl, 'main_soil_classification']
  classes$code[i] <- soildf[soildf$soil_classification == cl, 'code']
}

classes$code

levels(dataMaps) <- classes$mainclass
dataMaps.1 <- dataMaps
levels(dataMaps.1) <- classes$code

plot(dataMaps.1, main='Bodemkaart NL')

write.csv(classes, "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden/Bodemkaart/reclassified_soilclasses2.csv")

legend <- data.frame(class=NaN, mainclass=NaN)#, nrows=length(unique(mainclasses)))
for(uniqclass in unique(mainclasses)){
  
}
unique(mainclasses)

r <- dataMaps
a <- aggregate(r)


'Vz' %in% soildf$code

soildf['newcode'] <- NaN
soildf['newclass'] <- NaN

i=2

for(i in 1:length(soildf$code)){
  
  code = soildf$code[i]
  class = soildf$main_soil_classification[i]
  
  # 8 archetypen gebaseerd op codes
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
  
  # overige klassen gebaseerd op main classes
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
  
  soildf$newcode[i] <- newcode
  soildf$newclass[i] <- newclass
  
}


classes['newclass'] <- NaN
classes['newcode'] <- NaN

for(i in 1:length(classes$class)){
  cl <- as.character(classes$class[i])
  classes$newclass[i] <- soildf[soildf$soil_classification == cl, 'newclass']
  classes$newcode[i] <- soildf[soildf$soil_classification == cl, 'newcode']
}



write.csv(classes, "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden/Bodemkaart/reclassified_soilclasses3.csv")

names(classes)



levels(dataMaps) <- classes$newcode
plot(dataMaps, main='Soil map Netherlands')
