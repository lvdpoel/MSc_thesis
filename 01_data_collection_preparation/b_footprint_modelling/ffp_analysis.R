#
#This script calculates the footprints using Kljun footprint climatology functions.
#Because the file was too large, it was splitted in 3 parts - not ideal, but it worked.


## Cleanup
rm(list = ls(all.names = TRUE))

## Libs
library(tidyverse)  
library(sp)
library(raster, exclude = 'select')
library(sf)  
library(ggplot2)
library(fields)
library(rgdal)
library(directlabels)
library(metR)
library(ncdf4)
library(dplyr)
library(stringr)

# Get Kljun functions
sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/airborne_footprints/functions_kljun", full.names = T), source)

# Get data
filepath = "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/fp_meas_grhart.csv"
df <- read.csv(filepath, na='-9999') %>% data.frame() # 3529 rows


#### PREPARATION
summary(df)


# delete rows with NaNs and prevent errors in ffp_clim function
df <- na.omit(df) #3415 over
df <- df %>% filter(zm > 0)  %>% filter(zm<h) %>% filter(zm/ol >= -15.5) #3268 over

write.csv(df, 'C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne.csv')

# Optional input
domain <- c(-3000, 3000, -3000, 3000) # can be made larger to really be sure entire footprint is included
r <- seq(20, 80, 20) # contour percentages


#### Run functions
fp_values_all <- list()


df1 <- df[1:1000,]
df2 <- df[1001:2000,]
df3 <- df[2001:3268,]


start <- Sys.time()
dim(df3)
for (i in 1:nrow(df3)){
  row <- slice(df3, i)
  
  ffp_clim <- calc_footprint_FFP_climatology(zm = row$zm, z0 = NaN, umean = row$umean,
                                             h = row$h, ol = row$ol, sigmav = row$sigmav,
                                             ustar = row$ustar, wind_dir = row$wind_dir, 
                                             rslayer = 1, crop=0, r=r, fig=0, domain=domain)
  
  
  print(paste0('step ',i, '/', ))
  
  fp_values <- ffp_clim$fclim_2d
  raster_m <- raster::raster(t(fp_values[,ncol(fp_values):1]),
                             xmn = domain[1],
                             xmx = domain[2],
                             ymn = domain[3],
                             ymx = domain[4],
                             crs = 28992)
  
  # Get measurement coordinates --> lat lon point --> xy point:
  lonlat <- c(df3[i,]$Lon, df3[i,]$Lat)
  lonlat_sf <- st_point(lonlat) %>% st_sfc(crs=4326)
  xy <- st_transform(lonlat_sf , crs=28992) %>% st_coordinates()
  
  # Shift raster so (0,0) becomes measurement x,y (rijksdriehoek coördinaten)
  raster_rd = shift(raster_m, dx=xy[1], dy=xy[2])
  
  # Reproject raster to have lat-lon
  raster_latlon = projectRaster(raster_rd, crs = 4326)
  
  
  outfile <- paste0("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_values_rasters_2001-rest/raster3_",i,".nc")
  writeRaster(raster_latlon, outfile, overwrite=TRUE, format="CDF", varname="fp_value", varunit="-", 
              longname="test variable -- raster layer to netCDF", xname="lon", yname="lat")
  
}

end <- Sys.time()

print(end-start)
