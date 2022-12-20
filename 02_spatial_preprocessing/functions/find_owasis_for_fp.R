find_owasis_for_fp <-
  
  function(alldata, rasterno, owasisdf){
    
    
    # -----------------------------------------------------
    # Script to find correct owasis file number given a footprint raster number, based on the fp-measurement date.
    # Input: owasisdf: list with all owasis files, rasterno: number of the footprint raster.nc saved in folder
    # Output: OwfileNo: number of owasis file with correct date, Owfile: the actual file
    # Requires library(terra) and library(stringr) 
    # -------------------------------------------------------- 
    
    
    owasisdates <- as.numeric(owasisdf$yeardoy)
    
    # main data: all airborne measurements
    alldata <- read.csv('C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne.csv', header=T, row.names='X')
    
    # get year and doy from row in df
    year = str_trim(alldata[rasterno,]$Date) %>% substr(1,4)
    doy = ceiling(alldata[rasterno,]$DoY) %>% str_pad(3, pad='0')
    yeardoy = as.numeric(paste0(year,doy))
    
    fileno <- which(abs(owasisdates-yeardoy) == min(abs(owasisdates-yeardoy)))
    file <- owasisdf[fileno,1]
    
    return(list(OwfileNo = fileno, Owfile = file))
  }



