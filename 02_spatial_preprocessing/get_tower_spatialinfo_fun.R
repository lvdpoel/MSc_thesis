###
"""
Script that calculates the percentages of the present classes around the tower, 
within a radius based on 'x_90' per tower.

Input: tower data (.csv), self-made functions from folder called 'functions',
land use and soil map
Output: percentage of every class in the tower-footprint

"""

rm(list=ls())

# libraries
library(terra)
library(ggplot2)
library(ggmap)
library(foreign)
library(randomcoloR)
library(sf)
library(ggplot2)
library(pals)
library(gplots)

# get functions
sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

# get maps
path <- "~/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden"
maps <- importMaps(path)
LGN <- maps$LGN2020
soilmap <- maps$Bodemkaart

# read tower data 
lwH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/LangeweideHoog_Laura.csv", na.string='-9999')
lwL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/LangeweideLaag_Laura.csv", na.string='-9999')
zvH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/ZegveldVerhoogd_Laura.csv", na.string='-9999')
zvL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/ZegveldStandaard_Laura.csv", na.string='-9999')

lwH['site'] <- 'Langeweide_Hoog'
lwL['site'] <- 'Langeweide_Laag'
zvH['site'] <- 'Zegveld_Hoog'
zvL['site'] <- 'Zegveld_Laag'

radlwH = lwH$x_90  %>% as.numeric() %>% mean(na.rm=T)
radlwL = lwL$x_90  %>% as.numeric() %>% mean(na.rm=T)
radzvH = zvH$x_90  %>% as.numeric() %>% mean(na.rm=T)
radzvL = zvL$x_90  %>% as.numeric() %>% mean(na.rm=T)


## Zegveld coordinates
zvlat <- 52.137900000000002; zvlon <- 4.8400800000000004

## Langeweide coordinares
lwlat <- 52.036499999999997; lwlon <- 4.7920100000000003


get_tower_spatialinfo_fun <-
  function(lat,lon,margin,data,radius, dataname){
#----------------
#   Input: lat and lon of tower; margin to calculate tower area for (NOT the footprint),
#   radius to calculate the footprint for, dataname: 'LGN' or 'soilmap'
#   Output: % of every class present in the footprint
#-----------------
  
  # create tower area in correct shape
  twr_a <- twr_area(lat=lat, lon=lon, margin= margin)
  twr <- twr_a$TowerLocation
  plot_area <- twr_a$PlotArea
  fp_avg <- buffer(twr, radius)

  # prepare variables
  map <- data$raster
  name <- names(map)
  classes <- data$classes
  legend <- data$legend
  
  # crop map file to fp file size
  map.1 <- crop(map, plot_area, snap='out')

  # reclassification matrix
  rcl <- matrix(c(classes$oldID, classes$newID), ncol=2, nrow=nrow(classes))
  map.2 <-classify(map.1, rcl)
  levels(map.2) <- legend$newID

  #plot(map.2, type='classes')
  
  # calculate classes in average footprint
  a <- extract(map.2, fp_avg, list=T)[[1]]
  b <- as.data.frame(a)
  colnames(b)<-'newID'
  
  # prepare dataframe
  df <- as.data.frame(matrix(data=NA, nrow=1, ncol=nrow(legend))) 
  colnames(df) <- legend$ID
  
  # calculate sum of each class
  for(i in 1:nrow(legend)){
    ID <- legend$ID[i]
    newID <- legend$newID[i]
    perc_in_fp <- sum(b$newID == newID)/nrow(b)
    df[1,ID] <- perc_in_fp
  }
  
  # get correct colors
  colorsLGN <- c('limegreen', 'darkorange3', 'orange', 'turquoise1', 'olivedrab', 'darkolivegreen', 'dodgerblue', 'ivory4', 'yellow2', 'lightpink', 'darkolivegreen1', 'sienna')
  colorsSOIL <- hcl.colors(15, palette = "Earth")
  if(dataname == 'LGN'){legend['colors'] <- col2hex(colorsLGN)}
  if(dataname == 'soilmap'){legend['colors'] <- col2hex(colorsSOIL)}
  
  # add colors to map for plotting further on
  for(i in 1:nrow(classes)){
    ID = classes$ID[i]
    classes$colors[i] = legend$colors[legend$ID==ID]
  }
  
  return(list(Map=map.2, Classes=classes, Legend=legend, Contr_df=df))
}  


# example
y <- get_tower_spatialinfo_fun(lat=lwlat, lon=lwlon,margin=500,data=LGN,radius=radlwH, dataname='LGN')
df <- y$Contr_df; colnames(df)<-LGN$legend$ID

# add contribution row to tower dataframe
zvL_LGN_soil <- cbind(zvL_LGN_soil, df)



