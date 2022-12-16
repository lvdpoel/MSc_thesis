## Cleanup
rm(list = ls(all.names = TRUE))


## Libs
library(terra)
library(MODISTools)
library(MODIStsp)

folder <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/aqua/"
files <- list.files(folder, pattern= '.hdf')
files_ss <- files[1:4]

start = Sys.time()

# empty raster
NDVI_all <- rast()
i=1
for(i in 1:length(files)){
  file <- files[i]
  
  # first layer is NDVI
  NDVI <- sds(file)[1]
  
  # add year + doy as name
  names(NDVI) <- substring(file, 10, 16) 
  
  # reproject to have lat lon
  NDVI_latlon <- project(NDVI, 'epsg:4326', method = 'near', mask=FALSE, align=FALSE, gdal=TRUE) # takes 12 seconds
  values(NDVI_latlon) <- values(NDVI_latlon) / 10^8 # to make them between -0.2 and 1
  
  NDVI_all <- c(NDVI_all, NDVI_latlon)
  print(paste0(i,' / ', length(files), ' done!'))
}
end = Sys.time()
end-start


# save it all
outpath <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/"

writeRaster(NDVI_all, filename=paste0(outpath, 'NDVI_all.tiff'), overwrite=TRUE)
