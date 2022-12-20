# clean-up
# rm(list=ls())
# 
# library(terra)
# 
# mypathFFP <-  "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_values_rasters_1-1000/raster1.nc"
# fp <- rast(mypathFFP)
# #spatdata_all <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/test_spatdata_all.tiff")
# #myspatdata <- spatdata_all[[1]]
# 
# pathOWASIS <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/test_dataset/ontwateringsdiepte/Owasis.Groundwater.Netherlands_Owasis.Ontwateringsdiepte_2022-03-01T00h00m00s_2022-03-02T00h00m00s.tif"
# spatdata <- rast(pathOWASIS)

# ------------------------
# This function calculates the spatial temporal data values in a footprint, and returns those 
# in a raster format, and as the weighted average value. 
#
# Spatial temporal data is not the same as 'ruimtelijke data veenweiden', because:
# 1. the resolution is coarser (250m)
# 2. there is a time component (daily for OWASIS and 16-day for NDVI)
# 3. there are no categorical variables, only continuous
#
# Input: fp: footprint raster file, spatdata: some spatial data raster
# 
#
# Output: spatdata_in_fp: raster of spatdata values in footprint,  fp: raster of 
# footprint, spatdata_contr: contribution of spatdata to footprint
#
# Requires library(terra)
# It works for NDVI (MODIS) and OWASIS data (both 250mx250m resolutions)
# --------------------------
calc_spatdata_in_fp <- function(fp, spatdata){
  
  fp <- project(fp, crs(spatdata))
  fp[is.na(fp)] <- 0
  fp[fp<0] <- 0
  
  # crop modis/owasus file to fp file
  spatdata <- crop(spatdata, fp, snap='out')
  
  # make spatdata into vector of locations
  spatdata_locs <- as.polygons(spatdata, values = T, dissolve = F)
  
  # sum fp values for those locations            
  fp_cellsize <- 35.92811
  spatdata_locs[["fp_value"]] <- terra::extract(fp, spatdata_locs, fun= function(x) sum(x,na.rm=T))[[2]]*fp_cellsize/ prod(res(spatdata))
  
  # footprint values in same raster shape as spatdata
  fp.spatdata_locs <- rasterize(spatdata_locs, spatdata, field="fp_value")
  fp.final <- fp.spatdata_locs * prod(res(fp.spatdata_locs))
  fp.final[fp.final < 0.01] <- 0
  
  # calc spatdata per fp contribution
  spatdata_fp <- fp.final * spatdata
  spatdata_contr <- sum(as.data.frame(spatdata_fp)) / sum(as.data.frame(fp.final)) # to make fp sum up to 100%
  
  return(list(spatdata_in_fp=spatdata_fp,fp=fp.final, spatdata_contr=spatdata_contr))}

#test <- calc_spatdata_in_fp(mypathFFP, myspatdata)
#plot(test$spatdata_in_fp)
#test$spatdata_contr
#contr justified by the fact that we look at differences BETWEEN fp's not WITHIN
# 
# plot(spatdata)
# plot(fp.final)
# plot(fp)
