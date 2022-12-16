# script to read footprint files
# get date of footprint file
# for this date: get NDVI values
rm(list=ls())


library(terra)
library(readr)
library(stringr)

sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions/", full.names = T), source)

# get footprint files
fp.folder <- 'C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_rasters_all/'
fp.files <- list.files(fp.folder, pattern= '.nc')


ndvi_all <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/NDVI_all.tiff")

alldata <- read.csv('C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne.csv', header=T, row.names='X')
# NOG AANPASSEN
alldata['NDVI'] <- NaN


start=Sys.time()
for(i in 1:length(fp.files)){
  print(paste0(i, '/', length(fp.files)))
  fp.file <- fp.files[i]
  rasterno <- as.numeric(fp.file %>% str_remove('.nc')) 
  
  ## when calculating NDVI
  find <- find_ndvi_for_fp(rasterno=rasterno, ndvi_all=ndvi_all)
  myndvi <- find$Modfile
  #print(find$ModfileNo)
  
  mypathFP <- paste0(fp.folder, fp.file)
  myfp <- rast(mypathFP)
  
  ndvi_contr <- calc_ndvi_in_fp(fp=myfp, ndvi=myndvi)$ndvi_contr
  #print(rasterno, ndvi_contr)
  
  dfrow <- as.integer(rasterno)
  alldata[dfrow, 'NDVI'] <- ndvi_contr
  }
  
end=Sys.time()
print(end-start)


write.csv(alldata,'C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/fp_meas_grhart_ndvitest(all).csv', row.names = FALSE)


