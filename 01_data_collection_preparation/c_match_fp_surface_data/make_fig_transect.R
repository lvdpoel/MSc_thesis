################
# Script to make picture including
# 1. locations of towers
# 2. the transect of the flight
# 3. the tower footprints
# 4. a few airborne footprints
# on top of the land use map
################


# make nice figures
rm(list=ls())


# libraries
library(terra)
library(stringr)
# library(readr)
# library(tidyverse)
library(randomcoloR)
library(foreign)
library(gplots)
library(hash)
library(paletteer)


# get functions
sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

# get maps
path <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden"
maps <- importMaps(path)
LGN <- maps$LGN2020

# select dat from LGN
data <- LGN
map <- data$raster
qty <- names(map)
classes <- data$classes
legend <- data$legend
#legend <- rbind(c("NA",' ',"0", '#FFFFFF'), legend)

# get airborne data
airb_raw <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/airborne/airborne_data_1.csv")
transect <- na.omit(airb_raw[airb_raw$Date == ' 2020-03-26', c('Lon', 'Lat')])


# make spatial vector data of lat-lon points
m <- data.matrix(transect)
tr_latlon <- vect(m, type='points')
crs(tr_latlon) <- 'epsg:4326'
tr <- project(tr_latlon, 'epsg:28992')

# If data needs to be cropped, process can be speeded up by cropping BEFORE reclassifying: 

# crop LUC map to be slightly larger than the transect
xmargin = 10000
ymargin = 5000
map.1 <- crop(map, c(ext(tr)[1]-xmargin, ext(tr)[2]+xmargin,ext(tr)[3]-ymargin,ext(tr)[4]+ymargin))#, snap='near')

# Else:
# map.1<- map

# reclassification matrix
rcl <- matrix(c(classes$oldID, classes$newID), ncol=2, nrow=nrow(classes))
map.2 <-classify(map.1, rcl)
levels(map.2) <- legend$newID

plot(map.2, type='classes')#,levels=legend$newID)## WERKT!!!!!!!!!1

# selecteer alleen kleuren en namen die erin voorkomen
clrs_plot <- c(1,2,3,4,5,6,7,8,9,10, 11,12)


## Zegveld coordinates
zvlat <- 52.137900000000002; zvlon <- 4.8400800000000004

## Langeweide coordinates
lwlat <- 52.036499999999997; lwlon <- 4.7920100000000003

# Get RD coordinates using the function twr_area
zv <- twr_area(lat=zvlat, lon=zvlon, margin= 100)$TowerLocation
lw <- twr_area(lat=lwlat, lon=lwlon, margin =100)$TowerLocation


# you can also crop after reclassification
#margin = 5000
#map.3 <- crop(map.2, c(ext(tr)[1]-margin, ext(tr)[2]+margin,ext(tr)[3]-margin,ext(tr)[4]+margin))#, snap='near')

# selecteer alleen kleuren en namen die erin voorkomen
clrs_plot <- c(1,2,3,4,5,6,7,8,9,10, 11,12)

###
# NOW PLOT
##

plot(map.2, type='classes', col=legend$colors[clrs_plot], levels=legend$class[clrs_plot], 
   legend=F, main='Flight transect and tower footprints')

legend('bottomleft', legend=legend$class[clrs_plot], fill=legend$colors[clrs_plot], 
       cex=0.8, title='Land use classes')

plot(tr, add=T, cex=1,col='black')
lines(tr, lwd= 1.5, lt = 1)

sbar(d=10000,xy='bottomright', type='bar', divs=2, below='km', label=c(0, 5, 10),
     cex=1, xpd = T)


# Add towers and circular footprints
#points(zv, cex=0.5, pch=17, col='black') 
lines(buffer(zv, 260), lwd=2, col='black')
txt <- matrix(c(ext(zv)[1]-1500, ext(zv)[3]-1000), nrow = 1, ncol = 2) %>% vect(type='points') %>% text('Zegveld', cex=0.8)

#points(lw, cex=0.5,pch=17,col='black')
lines(buffer(lw, 250), lwd=2, col='black')
txt <- matrix(c(ext(lw)[1]-1500, ext(lw)[3]-1000), nrow = 1, ncol = 2) %>% vect(type='points') %>% text('Langeweide', cex=0.8)



### INCLUDING FOOTPRINTS

# get calculated footprints

# nu moet ik zorgen dat ik de goede fp bestanden vind voor de goede datum
fp.path1 <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_values_rasters_1-1000/"
fp.folder <- fp.path1
fp.files <- list.files(fp.folder, pattern= '.nc')
fp24 <- rast(paste0(fp.folder, fp.files[[24]]))
#fp25 <- rast(paste0(fp.folder, fp.files[[25]]))
fp26 <- rast(paste0(fp.folder, fp.files[[26]]))
fp27 <- rast(paste0(fp.folder, fp.files[[27]]))
fp28 <- rast(paste0(fp.folder, fp.files[[28]]))


# project footprints to have same crs as map

# #test if it works with 1 fp
# fpraster<- fp1
# fp <- project(fpraster, crs(map.2)) # duurt 4 sec
# fp[is.na(fp)] <- 0
# fp[fp<0] <- 0
# 
# 
# # makes fp resolution equal to map.1 resolution
# fp.final <- resample(fp,map.2,method = "bilinear")  
# 
# # WORKS FOR FP30
# fp.final[fp.final < 0.00000004] <- NA # 80%
# 
# plot(fp.final, add=TRUE,colNA=NULL, legend = FALSE, col='darkblue', alpha=0.4)

fps <- list(fp24,fp26,fp27,fp28)






######33 plot with footprints
plot(map.2, type='classes', col=legend$colors[clrs_plot], levels=legend$class[clrs_plot], 
     legend=F, main='Flight transect and footprints')

legend('bottomleft', legend=legend$class[clrs_plot], fill=legend$colors[clrs_plot], 
       cex=0.8, title='Land use classes')

plot(tr, add=T, cex=1,col='black')
lines(tr, lwd= 1.5, lt = 1)

sbar(d=10000,xy='bottomright', type='bar', divs=2, below='km', label=c(0, 5, 10),
     cex=1, xpd = T)

# Add towers and circular footprints
#points(zv, cex=0.5, pch=17, col='black') 
lines(buffer(zv, 260), lwd=2, col='black')
txt <- matrix(c(ext(zv)[1]-1500, ext(zv)[3]-1000), nrow = 1, ncol = 2) %>% vect(type='points') %>% text('Zegveld', cex=0.8)

#points(lw, cex=0.5,pch=17,col='black')
lines(buffer(lw, 250), lwd=2, col='black')
txt <- matrix(c(ext(lw)[1]-1500, ext(lw)[3]-1000), nrow = 1, ncol = 2) %>% vect(type='points') %>% text('Langeweide', cex=0.8)


# it works! do for all footprins
# for(fp in fps){
#   fp <- project(fp, crs(map.2)) # duurt 4 sec
#   fp[is.na(fp)] <- 0
#   fp[fp<0] <- 0
#   # makes fp resolution equal to map.1 resolution
#   fp.final <- resample(fp,map.2,method = "bilinear")  
#   fp.final[fp.final < 0.00000004] <- NA # 80%
#   plot(fp.final, add=TRUE,colNA=NULL, legend = FALSE, col='darkblue', alpha=0.4)
#   
#   
#}

fp28 <- rast(paste0(fp.folder, fp.files[[28]]))
for(i in 1:89){
  fp <- rast(paste0(fp.folder, fp.files[[i]]))
  fp <- project(fp, crs(map.2)) # duurt 4 sec
  fp[is.na(fp)] <- 0
  fp[fp<0] <- 0
  # makes fp resolution equal to map.1 resolution
  fp.final <- resample(fp,map.2,method = "bilinear")  
  fp.final[fp.final < 0.00000004] <- NA # 80%
  plot(fp.final, add=TRUE,colNA=NULL, legend = FALSE, col='darkblue', alpha=0.4)
  
}

