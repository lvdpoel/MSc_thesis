# 
rm(list=ls())

# get tower NDVI info
library(stringr)
library(terra)
library(beepr)

sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

NDVI_all <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/NDVI_all.tiff")


lwH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/lwH_ruimtdata.csv")#, na.string='-9999')
lwL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/lwL_ruimtdata.csv")#, na.string='-9999')
zvH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/zvH_ruimtdata.csv")#, na.string='-9999')
zvL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/zvL_ruimtdata.csv")#, na.string='-9999')

df_old <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/DataLangeweideZegveld/lw_zv_99_maps.csv")
df_1310 <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/modelling/final_airborne_tower/tower_shuffled_3009.csv", 
                    row.names ='X')

#lwH['site'] <- 'Langeweide_Hoog'
# lwL['site'] <- 'Langeweide_Laag'
# zvH['site'] <- 'Zegveld_Hoog'
# zvL['site'] <- 'Zegveld_Laag'

radlwH = lwH$x_90  %>% as.numeric() %>% mean(na.rm=T)
radlwL = lwL$x_90  %>% as.numeric() %>% mean(na.rm=T)
radzvH = zvH$x_90  %>% as.numeric() %>% mean(na.rm=T)
radzvL = zvL$x_90  %>% as.numeric() %>% mean(na.rm=T)




## Zegveld coordinates
zvlat <- 52.137900000000002; zvlon <- 4.8400800000000004

## Langeweide coordinares
lwlat <- 52.036499999999997; lwlon <- 4.7920100000000003


get_tower_ndvi <- function(df){#,dfname){ # df can be lwH, lwL, zvH or zvL
  for(i in 1:20){#nrow(df)){
    
    # if(dfname == 'lwH'){lat=lwlat; lon=lwlon; rad=radlwH}
    # if(dfname == 'lwL'){lat=lwlat; lon=lwlon; rad=radlwL}
    # if(dfname == 'zvH'){lat=zvlat; lon=zvlon; rad=radzvH}
    # if(dfname == 'zvL'){lat=zvlat; lon=zvlon; rad=radzvL}
    #if(df[i, 'site'] == 'lw'){lat=lwlat; lon=lwlon; rad=radlwH}
    lat = lwlat; lon=lwlon; rad=500
    print(paste0(i, '/', nrow(df)))
    
    # find correct ndvi file
    find <- find_ndvi_for_twr(row=i, alldata=df, ndvi_all=NDVI_all)
    myndvi <- find$Modfile
    
    t <- twr_area(lat=lat, lon=lon, margin=500)
    twr <- t$TowerLocation
    plot_area <- t$PlotArea
    
    ## everything with .1 is latlon, with .2 is RD 
    plot_area.1 <- project(plot_area, crs(myndvi)) # make plot_area in latlon
    myndvi.1 <- crop(myndvi, plot_area.1) # use latlon plot_area to crop myndvi
    myndvi.2 <- project(myndvi.1, crs(plot_area)) # make cropped latlon in RD
    
    plot(myndvi.2, main=i)}
    #points(twr)
    avg_fp.2 <- buffer(twr, rad)
    #lines(avg_fp.2)  
    
    # 
    # plot(myndvi.1, main='Langeweide, NDVI in latlon')
    # points(twr.1)
    # avg_fp.1 <- buffer(twr.1,100)
    # lines(avg_fp.1)
  
    a <- extract(myndvi.2, avg_fp.2)
    avgNDVI <- mean(a[,2]) 

    df[i,'NDVI'] <- avgNDVI
    
    #return(NDVI=avgNDVI)
  }
  return(df)
}

start=Sys.time()

zvL_ruimtdata_NDVI <- get_tower_ndvi(zvL, dfname='zvL')

new_tower_df <- get_tower_ndvi(df_1310)

end=Sys.time()
print(end-start)

beep(3)

write.csv(zvL_ruimtdata_NDVI2, "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/zvL_ruimtdata_NDVI.csv")

zvL_ruimtdata_NDVI[11000:11050,'NDVI']
zvL_ruimtdata_NDVI2 = zvL_ruimtdata_NDVI[-c(10745:nrow(zvL_ruimtdata_NDVI)), ]

dim(zvL_ruimtdata_NDVI2)
