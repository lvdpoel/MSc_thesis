find_ndvi_for_fp <-
  function(rasterno, ndvi_all){

# -----------------------------------------------------
# Script to find correct ndvi file number given a footprint raster number, based on the fp-measurement date.
# Input: ndvi_all: raster with every layer a modis ndvi raster, rasterno: number of the footprint raster.nc saved in folder
# Output: ModfileNo: number of modisfile with correct date, Modfile: the actual file
# Requires library(terra) and library(stringr) 
# -------------------------------------------------------- 
  
    # main data: all airborne measurements
    alldata <- read.csv('C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne.csv', header=T, row.names='X')
    
    # get year and doy from row in df
    year = str_trim(alldata[rasterno,]$Date) %>% substr(1,4)
    doy = ceiling(alldata[rasterno,]$DoY) %>% str_pad(3, pad='0')
    yeardoy = as.numeric(paste0(year,doy))
    
    # get modfileno and modfile with name closest to yeardoy
    moddates <- as.numeric(names(ndvi_all))
    modfileno <- which(abs(moddates-yeardoy) == min(abs(moddates-yeardoy)))
    modfile <- ndvi_all[[modfileno]]
    
    return(list(ModfileNo=modfileno, Modfile=modfile))
    
  }

#ndvi_all <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/test_NDVI_all.tiff")
#rasterno = 004
#test <- find_ndvi_for_fp(rasterno = rasterno, ndvi_all = ndvi_all )

