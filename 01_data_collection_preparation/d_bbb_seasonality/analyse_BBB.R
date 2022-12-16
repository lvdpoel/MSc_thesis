# read owasis data
# rm(list=ls())


library(stringr)
library(rlang)
library(terra)
library(lubridate)
library(beepr)
library(dplyr)

# Get lat-lon selection
air <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_data/airborne_lgn_soil_owasis_ndvi.csv")
air_20 <- sample_n(air, 20)

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



## Zegveld coordinates
zvlat <- 52.137900000000002; zvlon <- 4.8400800000000004

## Langeweide coordinares
lwlat <- 52.036499999999997; lwlon <- 4.7920100000000003

#%% other coords 1
lat1 <- 52.016884; lon1 <- 4.920149

#lat2 <- lwlat; lon2 <- 4.2000

lat3 <- lwlat; lon3 <- 4.4000

lat4 <- lwlat; lon4 <- 4.6000

lat5 <- lwlat; lon5 <- 4.8000

lat6 <- lwlat; lon6 <- 5.0000

lat7 <- lwlat; lon7 <- 5.2000

loc = 'zv'
t <- twr_area(lat=zvlat, lon=zvlon, margin=700) 
twr <- t$TowerLocation
plot_area <- t$PlotArea

df = data.frame(row.names = ow.bb.df$yeardoy)

start = Sys.time()
for(row in row.names(air_20)){
  print(row)
  
  lat <- air_20[row, 'Lat']
  lon <- air_20[row, 'Lon']
  loc = row
  
  t <- twr_area(lat=lat, lon=lon, margin=700) 
  twr <- t$TowerLocation
  plot_area <- t$PlotArea
  
  for(i in row.names(ow.owd.df)){
    #print('.')
    # BBB
    mybbfile = ow.bb.df[i,1]
    mybb <- rast(paste0(ow.bb.folder, mybbfile))
    
    #GWS
    mygrfile <- ow.gr.df[i,1]
    mygr <- rast(paste0(ow.gr.folder, mygrfile))
    
    #OWD
    myowdfile <- ow.owd.df[i,1]
    myowd <- rast(paste0(ow.owd.folder, myowdfile))
    
    
    yeardoy = ow.bb.df[i,2] 
    
    plot_area.1 <- project(plot_area, crs(mybb))
    
    mybb.1 <- crop(mybb, plot_area.1)
    mygr.1 <- crop(mygr, plot_area.1)
    myowd.1 <- crop(myowd, plot_area.1)  
  
    avg_fp <- buffer(twr, 500) # changed 
  
    avg_bb <- mean(extract(mybb.1, avg_fp)[,2])
    avg_gr <- mean(extract(mygr.1, avg_fp)[,2])
    avg_owd <- mean(extract(myowd.1, avg_fp)[,2])
    
    df[yeardoy,paste0('BBB_', loc)] <- avg_bb
    df[yeardoy,paste0('GWS_', loc)] <- avg_gr
    df[yeardoy, paste0('OWD_', loc)] <- avg_owd
      
  }
}

end = Sys.time()
print(end-start)
#%%

write.csv(df, "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/OWASIS_20locas.csv")
