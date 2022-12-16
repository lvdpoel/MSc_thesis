###
rm(list=ls())

# libraries
library(terra)
library(ggplot2)
library(ggmap)
library(foreign)
library(randomcoloR)
library(sf)
library(ggplot2)
library(pals)
library(gplots)

# import maps
# get functions
sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

# get maps
path <- "~/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden"
maps <- importMaps(path)
LGN <- maps$LGN2020
soilmap <- maps$Bodemkaart
GrWT <- maps$Grondwatertrap
Veendikte <- maps$Veendikte

NDVI_all <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/NDVI_all.tiff")
NDVI <- NDVI_all[[1]] # in lat lon



# get footprints
fp.path1 <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_values_rasters_1-1000/"
fp.folder <- fp.path1 # aanpassen
fp.files <- list.files(fp.folder, pattern= '.nc')
fp1 <- rast(paste0(fp.folder, fp.files[[1]]))
fp2 <- rast(paste0(fp.folder, fp.files[[85]]))


# read tower data 
lwH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/LangeweideHoog_Laura.csv", na.string='-9999')
lwL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/LangeweideLaag_Laura.csv", na.string='-9999')
zvH <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/ZegveldVerhoogd_Laura.csv", na.string='-9999')
zvL <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/ZegveldStandaard_Laura.csv", na.string='-9999')

lwH['site'] <- 'Langeweide_Hoog'
lwL['site'] <- 'Langeweide_Laag'
zvH['site'] <- 'Zegveld_Hoog'
zvL['site'] <- 'Zegveld_Laag'




## Zegveld coordinates
zvlat <- 52.137900000000002; zvlon <- 4.8400800000000004

## Langeweide coordinares
lwlat <- 52.036499999999997; lwlon <- 4.7920100000000003

## color palette
pal.bands(alphabet, alphabet2, cols25, glasbey, kelly, polychrome, 
          stepped, tol, watlington,
          show.names=FALSE)


calc_cls_tower <- function(lat, lon, data, site, margin=500, radius=100){ # lonlat of tower, data: map collection, site:name
  
  # create tower area in correct shape
  twr_a <- twr_area(lat=lat, lon=lon, margin= margin)
  twr <- twr_a$TowerLocation
  plot_area <- twr_a$PlotArea

  # prepare variables
  map <- data$raster
  name <- names(map)
  classes <- data$classes
  levels(map) <- classes$class
  legend <- data$legend
  
  # crop map file to fp file size
  map.1 <- crop(map, plot_area, snap='out')

  # calculate classes in average footprint
  a <- extract(map.1, fp_avg)
  colnames(a) <- c('count', 'class')
  df <- as.data.frame(matrix(data=NA, nrow=1, ncol=nrow(legend))) 
  colnames(df) <- legend$ID
  
  for(i in 1:nrow(legend)){
    cls <- legend$class[i]
    # print(ID)
    perc_in_fp <- sum(a$count[a$class == cls])/nrow(a)
    # print(sum(a$count[a$class == ID]))
    df[1,ID] <- perc_in_fp
  }
  
  return(list(contr=df,tower=twr, plotarea=plot_area))
}




df2 <- calc_cls_tower(lat = lwlat, lon=lwlon, data=LGN,  radius=100, site='Langeweide')

df3 <- calc_cls_tower(lat=lwlat, lon=lwlon, data=soilmap,margin=2000, radius=100, site='Langeweide')

df4 <- calc_cls_tower(lat=zvlat, lon=zvlon, data=soilmap, margin=5000,radius=100, site='Zegveld')

lwH.1 <- cbind(lwH, df)


## to do:
# make look nice                    mwa
# haal lelijke witte weg            X!
# zet iets op assen                 X
# plus afstand bar                  V
# zet tekst bij punt en cirkel      V
# bereken average footprint         gebaseerd op brief intro
# bereken contr per aanwezige class V

### COLORS
colorsLGN <- c('limegreen', 'darkorange3', 'orange', 'turquoise1', 'olivedrab', 'darkolivegreen', 'dodgerblue', 'ivory4', 'yellow2', 'lightpink', 'darkolivegreen1', 'sienna')
colorsSOIL <- hcl.colors(14, palette = "Earth")
#colorsGRWT <- hcl.colors(19, palette = "Fall")
legend['colors'] <- col2hex(colorsSOIL)


### PLOT
plot(map.1, main=site, #type='classes', levels=classes$class,
     legend=TRUE, sort=T, mar=NULL, col=legend$colors)


# add text for tower
points(twr, cex=2)
txt <- matrix(c(ext(twr)[1], ext(twr)[3]-40), nrow = 1, ncol = 2) %>% vect(type='points') %>% text('tower')

# add text for footprint
txt <- matrix(c(ext(twr)[1], ext(twr)[3]-170), nrow = 1, ncol = 2) %>% vect(type='points') %>% text('footprint', col='blue')
fp_avg <- buffer(twr, radius)
lines(fp_avg, col='blue', lwd=2)

sbar(d=500,xy='bottomright', type='bar', divs=2, below='meters', label=c(0, 250, 1000),
     cex=1, xpd = T)

