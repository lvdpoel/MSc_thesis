#------------
# fp_analysis ruimtelijk data: soil and land use maps
# script computes percentages of present classes in footprint 

# Input: land use and soil maps,  all footprint files (.nc), 
# self-made functions from folder 'functions', airborne measurements data (.csv)

# Output: airborne dataframe, with for every measurement, the present percentage of
# every land use and soil class
#-----------------

rm(list=ls())


######## 
# Libraries

library(terra)
library(stringr)
library(readr)
library(tidyverse)
library(randomcoloR)
library(foreign)
library(beepr)
library(gplots)

#########################################
#                                       #
# Get all necessary data and functions  #
#                                       #
#########################################

# get functions
sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

# get maps
path <- "~/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden"
maps <- importMaps(path)
LGN <- maps$LGN2020
soilmap <- maps$Bodemkaart


fp.folder <- 'C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_rasters_all/'
fp.files <- list.files(fp.folder, pattern= '.nc')


alldata <- read.csv('C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne.csv', header=T, row.names='X')

# create df to store calculated data
df_out <- data.frame(matrix(ncol = ncol(alldata) + nrow(LGN$legend) + nrow(soilmap$legend), nrow = nrow(alldata)))
colnames(df_out) <- c(colnames(alldata), LGN$legend$ID,  soilmap$legend$ID)

fp.file = '3258.nc'
start=Sys.time()
for(i in 1:length(fp.files)){
  print(paste0(i, '/', length(fp.files)))
  fp.file <- fp.files[i]
  rasterno <- as.numeric(fp.file %>% str_remove('.nc')) 
  

  mypathFP <- paste0(fp.folder, fp.file)
  myfp <- rast(mypathFP)
  
  # calc LGN contributions
  lgn <- calc_ruimt_data_in_fp(data = LGN, fpraster = myfp, cat=T) # aanpassen
  
  #  calc soil contributions
  soil <- calc_ruimt_data_in_fp(data = soilmap, fpraster = myfp, cat=T) # aanpassen
  
  dfrow <- as.integer(rasterno)
  
  # save in df_out
  df_out[dfrow,] <- cbind(alldata[dfrow,],lgn,soil)
}  


end=Sys.time()
print(end-start)

pathout <- 'C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne_lgn_soil.csv'
write.csv(df_out, pathout, row.names = TRUE) 
beep(3)
