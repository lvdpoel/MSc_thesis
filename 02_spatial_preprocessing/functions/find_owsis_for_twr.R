### script to find NDVI file for date in tower measurement
find_owasis_for_twr <-
  function(rasterno=NULL,row=1, alldata=lwH, owasisdf){
    
    # -----------------------------------------------------
    # Script to find correct owasis file number given the datetime of the tower measurement
    # Input: owasis df with (column1) name owasis files and (column2) yeardoy 
    # alldata: tower measurements
    # Output: ModfileNo: number of modisfile with correct date, Modfile: the actual file
    # Requires library(terra) and library(stringr) 
    # het werkt
    # -------------------------------------------------------- 
    
    
    # if 'alldata' is all airborne measurements file:
    # get year and doy from row in df
    # year = str_trim(alldata[rasterno,]$Date) %>% substr(1,4)
    # doy = ceiling(alldata[rasterno,]$DoY) %>% str_pad(3, pad='0')
    # yeardoy = as.numeric(paste0(year,doy))
    
    # if 'alldata' is tower measurements
    datetime <- alldata[row, 'datetime'] %>% as.POSIXct(format="%Y-%m-%d %H:%M:%S", tz="UTC")
    year <- strftime(datetime, format='%Y')
    doy <- strftime(datetime, format = "%j") %>% str_pad(3, pad='0')
    yeardoy <- as.numeric(paste0(year, doy))
    
    
    # get modfileno and modfile with name closest to yeardoy
    owasisdates <- as.numeric(owasisdf$yeardoy)    
    fileno <- which(abs(owasisdates-yeardoy) == min(abs(owasisdates-yeardoy)))
    file <- owasisdf[fileno,1]
    
    return(list(OwfileNo = fileno, Owfile = file))
    
  }


