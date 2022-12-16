# 
rm(list=ls())



# Libraries
library(stringr)
library(terra)
library(beepr)
library(lubridate)
library(tibble)
library(dplyr)

sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

#######################
# PREPARE OWASIS DATA #
#######################

# Create dataframes with filenames 
# And save year + day of year for every filename

# Bodemberging
ow.bb.folder <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/complete_dataset/Beschikbare.Bodemberging/"
ow.bb.files <- list.files(ow.bb.folder, pattern= '.tif')
ow.bb.df <- as.data.frame(ow.bb.files)

for(i in 1:nrow(ow.bb.df)){
  string <- ow.bb.df[i,1]
  ow.bb.df[i,'yeardoy'] = paste0(substr(string, 64,67), str_pad(yday(substr(string, 64,73)), 3, pad='0'))
  ow.bb.df[i,'yeardoy'] = as.numeric(ow.bb.df[i,'yeardoy'])
}


# ## Grondwaterstand
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



##################
# Get tower data #
##################

## OLD DATA
lwH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/lwH_ruimtdata_NDVI_owasis.csv")#, na.string='-9999')
lwL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/lwL_ruimtdata_NDVI_owasis.csv")#, na.string='-9999')
zvH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/zvH_ruimtdata_NDVI_owasis.csv")#, na.string='-9999')
zvL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/zvL_ruimtdata_NDVI_owasis.csv")#, na.string='-9999')
 
# lwH = lwH %>% add_column(BBB = NA) %>% add_column(GWS = NA)
# lwL %>% add_column(BBB = NA) %>% add_column(GWS = NA)
# zvH %>% add_column(BBB = NA) %>% add_column(GWS = NA)
# zvL %>% add_column(BBB = NA) %>% add_column(GWS = NA)

#lwH['OWD'] = NA
#lwL['OWD'] = NA
#zvH['OWD'] = NA
#zvL['OWD'] = NA


radlwH = lwH$x_90  %>% as.numeric() %>% mean(na.rm=T)
radlwL = lwL$x_90  %>% as.numeric() %>% mean(na.rm=T)
radzvH = zvH$x_90  %>% as.numeric() %>% mean(na.rm=T)
radzvL = zvL$x_90  %>% as.numeric() %>% mean(na.rm=T)


## Zegveld coordinates
zvlat <- 52.137900000000002; zvlon <- 4.8400800000000004

## Langeweide coordinares
lwlat <- 52.036499999999997; lwlon <- 4.7920100000000003


# or, when joining datasets is already done: take all towerdat a together
towerdata <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/DataLangeweideZegveld/lw_zv_99_maps.csv", 
                      header=TRUE)
rownames(towerdata) <- towerdata$X 
towerdata$X <- NULL



########################################
# Function to caculate BBB,GWS and OWD #
# for every measurement                #
########################################

i=100;df=lwH;dfname='lwH'

df=towerdata

get_tower_owasis <- function(df){#,dfname){ # df can be lwH, lwL, zvH or zvL
  for(i in 1:5){#nrow(df)){
    
    # for when data is still in different dataframes
    # if(dfname == 'lwH'){lat=lwlat; lon=lwlon; rad=radlwH}
    # if(dfname == 'lwL'){lat=lwlat; lon=lwlon; rad=radlwL}
    # if(dfname == 'zvH'){lat=zvlat; lon=zvlon; rad=radzvH}
    # if(dfname == 'zvL'){lat=zvlat; lon=zvlon; rad=radzvL}
     
    # if it's all together
    # can be made faster but for now not necessary
    if(df[i, 'site'] == 'lwH' | df[i, 'site'] == 'lwL'| df[i, 'site'] == 'lw'){lat=lwlat; lon=lwlon}
    if(df[i, 'site'] == 'zvH' | df[i, 'site'] == 'zvL' | df[i, 'site'] == 'zv'){lat=zvlat; lon=zvlon}

    print(paste0(i, '/', nrow(df)))
    
    # Plot tower area
    start = Sys.time()
    t <- twr_area(lat=lat, lon=lon, margin=700) 
    twr <- t$TowerLocation
    plot_area <- t$PlotArea
    
    # BBB
    mybbfile <- find_owasis_for_twr(row=i, alldata=df, owasisdf= ow.bb.df)$Owfile
    mybb <- rast(paste0(ow.bb.folder, mybbfile))
    
    # GWS
    mygrfile <- find_owasis_for_twr(row=i, alldata=df, owasisdf= ow.gr.df)$Owfile
    mygr <- rast(paste0(ow.gr.folder, mygrfile))
     
    # OWD
    myowdfile <- find_owasis_for_twr(row=i, alldata=df, owasisdf= ow.owd.df)$Owfile
    myowd <- rast(paste0(ow.owd.folder, myowdfile))
    
    # crop BBB and GWS files
    plot_area.1 <- project(plot_area, crs(mygr))
    mybb.1 <- crop(mybb, plot_area.1)
    mygr.1 <- crop(mygr, plot_area.1)
    myowd.1 <- crop(myowd, plot_area.1)
    
    # calculate average footprint around tower
    avg_fp <- buffer(twr, 500) # changed 

    avg_bb <- mean(extract(mybb.1, avg_fp)[,2])
    avg_gr <- mean(extract(mygr.1, avg_fp)[,2])
    avg_owd <- mean(extract(myowd.1, avg_fp)[,2])

    df[i,'BBB'] <- avg_bb
    df[i, 'GWS'] <- avg_gr
    df[i, 'OWD'] <- avg_owd
  }
  return(df)
}

start=Sys.time()


# with different files for location
#zvL_ruimtdata_NDVI_owasis_owd <- get_tower_owasis(zvL, dfname='zvL')
#write.csv(zvL_ruimtdata_NDVI_owasis_owd, "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/zvL_ruimtdata_NDVI_owasis_owd.csv")

newdf = get_tower_owasis(towerdata)
write.csv(newdf, "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/towerdata_all_99Q_owd_2606_areas.csv")

end=Sys.time()
print(end-start)

beep(3)



## PLOT ONLY LANGE WEIDE
map = GWS

# for OWD use: "grDevices::Green-Brown"
plot(mygr.1, legend=T,col= paletteer_c("ggthemes::Blue", 30), 
     main = 'Langeweide',plg=list(title='Ground water level (m-NAP)'))

# add text for tower
points(twr, cex=2)
txt <- matrix(c(ext(twr)[1], ext(twr)[3]-70), nrow = 1, ncol = 2) %>% vect(type='points') %>% text('tower')


# add text for footprint
txt <- matrix(c(ext(twr)[1], ext(twr)[3]-300), nrow = 1, ncol = 2) %>% vect(type='points') %>% text('footprint', col='black')
fp_avg <- buffer(twr, 252)
lines(fp_avg, col='black', lwd=2)

sbar(d=200,xy='bottomright', type='bar', divs=2, below='meters', label=c(0, 100, 200),
     cex=1, xpd = T)

