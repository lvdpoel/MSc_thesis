# make nice figures
rm(list=ls())


# libraries
library(terra)
library(stringr)
# library(readr)
# library(tidyverse)
library(randomcoloR)
library(foreign)
library(gplots)
library(hash)
library(paletteer)



# get functions
sapply(list.files(path = "C:/Users/l_vdp/Documents/MSc_Thesis/scripts/preprocessing/functions", full.names = T), source)

# get maps
path <- "~/MSc_Thesis/data/preprocessing/ruimtelijke_data_veenweiden"
maps <- importMaps(path)
LGN <- maps$LGN2020
soilmap <- maps$Bodemkaart
GrWT <- maps$Grondwatertrap
Veendikte <- maps$Veendikte

NDVI_all <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/modis/NDVI_all.tiff"
NDVI <- rast(NDVI_all)[[1]]

BBBjuni <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/complete_dataset/Beschikbare.Bodemberging/Owasis.Groundwater.Netherlands_Owasis.Beschikbare.Bodemberging_2019-06-21T00h00m00s_2019-06-22T00h00m00s.tif")
BBBdec <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/complete_dataset/Beschikbare.Bodemberging/Owasis.Groundwater.Netherlands_Owasis.Beschikbare.Bodemberging_2020-12-21T00h00m00s_2020-12-22T00h00m00s.tif")
GWS <- rast("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/owasis/complete_dataset/Grondwaterstand/Owasis.Groundwater.Netherlands_Owasis.Grondwaterstand_2019-06-20T00h00m00s_2019-06-21T00h00m00s.tif")

fp.path1 <- "C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/ffp_output/fp_values_rasters_1-1000/"
fp.folder <- fp.path1
fp.files <- list.files(fp.folder, pattern= '.nc')
fp1 <- rast(paste0(fp.folder, fp.files[[1]]))
fp30 <- rast(paste0(fp.folder, fp.files[[30]]))
fp100 <- rast(paste0(fp.folder, fp.files[[100]]))
fp666 <- rast(paste0(fp.folder, fp.files[[666]]))
fpraster <- fp1

# save attributes to variables
data <- GWS
map <- data$raster
qty <- names(map)
classes <- data$classes
legend <- data$legend

# for OWASIS:
map <- data


fp <- project(fpraster, crs(map)) # duurt 4 sec
fp[is.na(fp)] <- 0
fp[fp<0] <- 0

classes['newID'] <- NaN

# save new ID's in classes
for(i in 1:nrow(classes)){
  ID <- classes$ID[i]
  classes$newID[i] = legend$newID[legend$ID==ID]
}

# make colors
colorsLGN <- c('limegreen', 'darkorange3', 'orange', 'turquoise1', 'olivedrab', 'darkolivegreen', 'dodgerblue', 'ivory4', 'yellow2', 'lightpink', 'darkolivegreen1', 'sienna')
colorsSOIL <- hcl.colors(15, palette = "Earth")
colorsGRWT <- hcl.colors(19, palette = "Fall")



legend['colors'] <- col2hex(colorsSOIL)

classes['colors']<-NaN
for(i in 1:nrow(classes)){
  newID = classes$newID[i]
  classes$colors[i] = legend$colors[legend$newID==newID]
}


# CROP MAP
map.1 <- crop(map, fp, snap='out')


############## TRY OUT RECLASSIFY

# reclassification matrix
rcl <- matrix(c(classes$oldID, classes$newID), ncol=2, nrow=nrow(classes))
map.2 <-classify(map.1, rcl)
levels(map.2) <- legend$newID

plot(map.2, type='classes')#, levels=legend$newID)## WERKT!!!!!!!!!1


# selecteer alleen kleuren en namen die erin voorkomen
# of sla even slim op:
# fp1: LGN
#cls_plot <- c(1,2,4,5,6,7,8,11,12)
# soil:
#cls_plot <- c(1,3,4,6,13,14)

#fp30 soil
#cls_plot <- c(3,4,11,12,13)

#fp666: soil
#cls_plot <- c(2,4,6,13,14)
# lgn
#cls_plot <- c(1,2,3,4,5,6,7,8,11,12)

# fp50: LGN
#cls_plot <- c(1,2,3,5,6,7,8,11,12)
# fp50: soil
#cls_plot <- c(3,4,12,13)

#plot(map.2, type='classes', col=legend$colors[cls_plot], levels=legend$class[cls_plot])




############## FINISH TRY OUT



# makes fp resolution equal to map.1 resolution
fp.final <- resample(fp,map.2,method = "bilinear")  


# for owasis:
map.2 = map.1
fp.final <- fp

# # WORKS FOR FP1
fp.final[fp.final < 0.0000001] <- NA # 80%
fp.final2 <- fp.final
fp.final2[fp.final2 < 0.000001005] <- NA # 60%
fp.final3 <- fp.final
fp.final3[fp.final3 <0.000003 ] <- NA # 40%


# fp.final=fp
# WORKS FOR FP30
# fp.final[fp.final < 0.00000004] <- NA # 80%
# fp.final2 <- fp.final
# fp.final2[fp.final2 < 0.00000030] <- NA # 60%
# fp.final3 <- fp.final
# fp.final3[fp.final3 <0.0000009 ] <- NA # 40%
# sum(as.data.frame(fp.final3 * 25))


# WORKS FOR FP50
# fp.final[fp.final < 0.00000005] <- NA # 80%
# fp.final2 <- fp.final
# fp.final2[fp.final2 < 0.000000250] <- NA # 60%
# fp.final3 <- fp.final
# fp.final3[fp.final3 <0.000000805 ] <- NA # 40%
# 
# # fp.final=fp
# # WORKS FOR FP666
# fp.final[fp.final < 0.0000001] <- NA # 80%
# fp.final2 <- fp.final
# fp.final2[fp.final2 < 0.00000050] <- NA # 60%
# fp.final3 <- fp.final
# fp.final3[fp.final3 <0.0000015 ] <- NA # 40%

#sum(as.data.frame(fp.final3 * 25))
plot(fp.final, main='fp.final', col='darkmagenta')
plot(fp.final2, main='fp.final2', col='pink', add=T)
plot(fp.final3, main='fp.final3', col='magenta1', add=T)
# 



# plot
#######################
# DIT WERKT FOR CATEGORICAL
#plot(map.2, type='classes', col=legend$colors[cls_plot], levels=legend$class[cls_plot], 
  #   legend=F, main='Airborne footprint over soil classes')

#legend('topleft', legend=legend$class[cls_plot], fill=legend$colors[cls_plot], cex=0.8, title='Soil classes')


plot(map.1, main='Airborne footprint over grondwaterstand', 
     col= paletteer_c("ggthemes::Classic Orange-White-Blue Light", 30), legend=T, plg=list(title='GWS'))
plot(fp.final, add=TRUE,colNA=NULL, legend = FALSE, col='darkblue', alpha=0.4)
plot(fp.final2, add=TRUE, colNA=NULL, legend=FALSE, col='blue', alpha=0.4)
plot(fp.final3, add=TRUE, colNA=NULL, legend=FALSE, col= 'deepskyblue', alpha=0.4)
sbar(1000, xy='bottomright', below='meters', label = c(0,500,1000), type = 'bar', lonlat=F)

# for fp 1:
legend(x=121350,y=463330, legend=c('40%', '60%', '80%'),  fill=c('deepskyblue', 'blue', 'darkblue'), bty='n', horiz=T, cex=0.8)

# for fp30
#legend(x=125000,y=441000, legend=c('40%', '60%', '80%'),  fill=c('deepskyblue', 'blue', 'darkblue'), bty='n', horiz=T, cex=0.8)


# for fp666:
#legend(x=135900,y=435900,legend=c('40%', '60%', '80%'),  fill=c('deepskyblue', 'blue', 'darkblue'), bty='n', horiz=T, cex=0.8)
# for latlon
#legend(x=5.11,y=51.912,legend=c('40%', '60%', '80%'),  fill=c('deepskyblue', 'blue', 'darkblue'), bty='n', horiz=T, cex=0.8)

# for fp = 50
#legend(x=126800,y=448250, legend=c('80%','60%', '40%'), fill=c('darkblue', 'blue', 'deepskyblue'), bty='n')


