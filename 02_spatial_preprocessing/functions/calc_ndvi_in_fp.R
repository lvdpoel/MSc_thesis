calc_ndvi_in_fp <- function(fp, ndvi){
  
# clean-up
#  rm(list=ls())

# library(terra)

#mypathFFP <-  "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_values_rasters_1-1000/raster1.nc"
#ndvi_all <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/test_NDVI_all.tiff")
#myndvi <- ndvi_all[[1]]

# ------------------------
# This function calculates the ndvi values in a footprint, and returns those 
# in a raster format, as the weighted average value
#
# Input: fp: footprint raster file, ndvi: one ndvi raster from
# ndvi_all list, 
#
# Output: ndvi_in_fp: raster of ndvi values in footprint,  fp: raster of 
# footprint, same shape as ndvi, ndvi_contr: contribution of ndvi to footprint
#
# Requires library(terra)
# --------------------------

  fp[is.na(fp)] <- 0
  fp[fp<0] <- 0
  
  # crop modis file to fp file
  ndvi <- crop(ndvi,fp, snap='out')
  
  # make ndvi into vector of locations
  ndvi_locs <- as.polygons(ndvi, values = T, dissolve = F) 
  
  # sum fp values for those locations            
  fp_cellsize <- 35.92811
  ndvi_locs[["fp_value"]] <- extract(fp, ndvi_locs, fun= function(x) sum(x,na.rm=T))[[2]]*fp_cellsize/prod(res(ndvi))
  
  # footprint values in same raster shape as ndvi
  fp.ndvi_locs <- rasterize(ndvi_locs, ndvi, field="fp_value")
  fp.final <- fp.ndvi_locs * prod(res(fp.ndvi_locs))
  fp.final[fp.final < 0.01] <- 0 
  
  # calc ndvi per fp contribution
  ndvi_fp <- fp.final * ndvi
  ndvi_contr <- sum(as.data.frame(ndvi_fp))# /sum(as.data.frame(fp.final)) #added too late for thesis
  
  return(list(ndvi_in_fp=ndvi_fp,fp=fp.final, ndvi_contr=ndvi_contr))}




