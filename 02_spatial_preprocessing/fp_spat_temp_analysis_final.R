#------------
# script that calculates average of OWASIS variables and NDVI in airborne footprint,
# which is based on Kljun's footprint model (2015)

# Input: all OWASIS data (.tif), all NDVI data (.tiff), all footprint files (.nc), 
# self-made functions from folder 'functions', airborne measurements data (.csv)

# Output: airborne dataframe, with for every measurement, average NDVI, and 
# OWASIS variables (OWD, GWS and BBB).
#---------------


# read owasis data
rm(list=ls())


library(stringr)
library(rlang)
library(terra)
library(lubridate)
library(beepr)


################
# PREPARATION #
###############

# Prepare OWASIS data

# Create dataframes with filenames 
# And save year + day of year for every filename

## Bodemberging
ow.bb.folder <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/complete_dataset/Beschikbare.Bodemberging/"
ow.bb.files <- list.files(ow.bb.folder, pattern= '.tif')
ow.bb.df <- as.data.frame(ow.bb.files)

for(i in 1:nrow(ow.bb.df)){
  string <- ow.bb.df[i,1]
  ow.bb.df[i,'yeardoy'] = paste0(substr(string, 64,67), str_pad(yday(substr(string, 64,73)), 3, pad='0'))
  ow.bb.df[i,'yeardoy'] = as.numeric(ow.bb.df[i,'yeardoy'])
}


## Grondwaterstand
ow.gr.folder <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/complete_dataset/Grondwaterstand/"
ow.gr.files <- list.files(ow.gr.folder, pattern= '.tif')
ow.gr.df <- as.data.frame(ow.gr.files)

for(i in 1:nrow(ow.gr.df)){
  string <- ow.gr.df[i,1]
  ow.gr.df[i,'yeardoy'] = paste0(substr(string, 55,58), str_pad(yday(substr(string, 55,64)), 3, pad='0'))
  ow.gr.df[i,'yeardoy'] = as.numeric(ow.gr.df[i,'yeardoy'])
}


## Ontwateringsdiepte
ow.owd.folder <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/complete_dataset/Ontwateringsdiepte/"
ow.owd.files <- list.files(ow.owd.folder, pattern= '.tif')
ow.owd.df <- as.data.frame(ow.owd.files)

for(i in 1:nrow(ow.owd.df)){
  string <- ow.owd.df[i,1]
  ow.owd.df[i,'yeardoy'] = paste0(substr(string, 58,61), str_pad(yday(substr(string, 58,67)), 3, pad='0')) 
  ow.owd.df[i,'yeardoy'] = as.numeric(ow.owd.df[i,'yeardoy'])
}

# get NDVI data
ndvi_all <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/NDVI_all.tiff")

# get functions
sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions/", full.names = T), source)


# get airborne data
alldata <- read.csv('C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne.csv', header=T, row.names='X')

alldata['BBB'] <- NaN
alldata['GWS'] <- NaN
alldata['OWD'] <- NaN
alldata['NDVI'] <- NaN

# get footprint files
fp.folder <- 'C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_rasters_all/'
fp.files <- list.files(fp.folder, pattern= '.nc')

##################################
# calculate average values in fp #
##################################

df_out <- alldata

start=Sys.time()
for(i in 765:length(fp.files)){
  print(paste0(i, '/', length(fp.files)))
  fp.file <- fp.files[[i]]
  rasterno <- as.numeric(fp.file %>% str_remove('.nc')) 
  
  # get FP
  mypathFP <- paste0(fp.folder, fp.file)
  myfp <- rast(mypathFP)
  
  # find correct file and calculate contribution
  
  # for BBB
  print('one...')
  mybbfile <- find_owasis_for_fp(rasterno=rasterno, owasisdf = ow.bb.df)$Owfile
  mybb <- rast(paste0(ow.bb.folder, mybbfile))
  bb_contr <- calc_spatdata_in_fp(fp=myfp, spatdata=mybb)$spatdata_contr
  
  # for GR
  print('two...')
  mygrfile <- find_owasis_for_fp(rasterno=rasterno, owasisdf =ow.gr.df)$Owfile
  mygr <- rast(paste0(ow.gr.folder, mygrfile))
  gr_contr <- calc_spatdata_in_fp(fp=myfp, spatdata = mygr)$spatdata_contr

  # for OWD
  print('three...')
  myowdfile <- find_owasis_for_fp(rasterno=rasterno, owasisdf =ow.owd.df)$Owfile
  myowd <- rast(paste0(ow.owd.folder, myowdfile))
  owd_contr <- calc_spatdata_in_fp(fp=myfp, spatdata = myowd)$spatdata_contr
  
  # NDVI
  print('four...')
  myndvifile <- find_ndvi_for_fp(rasterno=rasterno, ndvi_all=ndvi_all)
  myndvi <- myndvifile$Modfile
  ndvi_contr <- calc_spatdata_in_fp(fp=myfp, spatdata=myndvi)$spatdata_contr
  
  # save in df_out
  dfrow <- as.integer(rasterno)
  df_out[dfrow,'BBB'] <- bb_contr
  df_out[dfrow, 'GWS'] <- gr_contr
  df_out[dfrow,'OWD'] <- owd_contr
  df_out[dfrow, 'NDVI'] <- ndvi_contr
  
}  

pathout <- 'C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne_owasis_ndvi.csv'
write.csv(df_out,pathout, row.names=TRUE)

end=Sys.time()
print(end-start)

beep(3)
