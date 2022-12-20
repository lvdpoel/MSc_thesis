# 
"""
This script calculates the average NDVI in an area (radius = 500) around the footprint
using the NDVI file closest in time. It uses the function 'find_ndvi_for_twr' to
get the correct NDVi file.

Input: all NDVI data (.tiff), self-made functions in folder 'functions' (.R), 
towerdata (.csv)
# Output: towerdata with an extra column with average NDVI value (.csv)

"""


rm(list=ls())

# libs
library(stringr)
library(terra)
library(beepr)


# get functions
sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

# get data
NDVI_all <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/NDVI_all.tiff")

lwH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/lwH_ruimtdata.csv")#, na.string='-9999')
lwL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/lwL_ruimtdata.csv")#, na.string='-9999')
zvH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/zvH_ruimtdata.csv")#, na.string='-9999')
zvL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/zvL_ruimtdata.csv")#, na.string='-9999')


## Zegveld coordinates
zvlat <- 52.137900000000002; zvlon <- 4.8400800000000004

## Langeweide coordinares
lwlat <- 52.036499999999997; lwlon <- 4.7920100000000003


get_tower_ndvi <- function(lat, lon, df){ # df can be lwH, lwL, zvH or zvL
  for(i in 1:nrow(df)){

    print(paste0(i, '/', nrow(df)))
    
    # find correct ndvi file
    find <- find_ndvi_for_twr(row=i, alldata=df, ndvi_all=NDVI_all)
    myndvi <- find$Modfile
    
    # make raster of tower location using function twr_area
    t <- twr_area(lat=lat, lon=lon, margin=500)
    twr <- t$TowerLocation
    plot_area <- t$PlotArea
    
    ## everything with .1 is latlon, with .2 is RD 
    plot_area.1 <- project(plot_area, crs(myndvi)) # make plot_area in latlon
    myndvi.1 <- crop(myndvi, plot_area.1) # use latlon plot_area to crop myndvi
    myndvi.2 <- project(myndvi.1, crs(plot_area)) # make cropped latlon in RD
    
    # calculate average in circle around tower
    avg_fp.2 <- buffer(twr, rad)
    a <- extract(myndvi.2, avg_fp.2)
    avgNDVI <- mean(a[,2]) 

    df[i,'NDVI'] <- avgNDVI
  }
  return(df)
}

# example:
zvL_ruimtdata_NDVI <- get_tower_ndvi(lwlat, lwlon, zvL)

write.csv(zvL_ruimtdata_NDVI, "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/zvL_ruimtdata_NDVI.csv")

