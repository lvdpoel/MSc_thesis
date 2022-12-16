# -----------------------------------
# function to import maps from ruimtelijke data veenweiden
# input: tif files for maps and classes documents
# some categorical maps are reclassified to have fewer classes
# output: object with all maps, classes and legends stored
# -----------------------------------




# importMaps
importMaps <- function(path) {
  
  maps <- NULL
  
  ## Read in
  ## LGN2020
  LGNpath <- paste0(path, '/Landgebruik_LGN2020')
  dataMaps <- rast(paste0(LGNpath , '/LGN2020.tif'))
  # classes <- read.csv(paste0(LGNpath, '/LGN2020_legend.csv'))
  classes <- read.csv(paste0(LGNpath, '/LGN2020_reclassified.csv'), sep=';')
  legend <- read.csv(paste0(LGNpath, '/LGN2020_newlegend.csv'), sep=';')
  
  # Wietse's colors
  # colors <- read.csv(paste0(LGNpath , '/LGN2020_colors.dat'), sep = "")
  # colors <- rgb(colors$X0,colors$X0.1,colors$X0.2,maxColorValue=255)
  # classes <- cbind(classes, colors)
  # rm(colors)
  
  # set new ID and class-colors in legend
  legend['newID'] <- 1:nrow(legend)
  colorsLGN <- c('limegreen', 'darkorange3', 'orange', 'turquoise1', 'olivedrab', 'darkolivegreen', 'dodgerblue', 'ivory4', 'yellow2', 'lightpink', 'darkolivegreen1', 'sienna')
  legend['colors'] <- col2hex(colorsLGN)
  
  # add to classes
  classes['newID'] <- NaN; classes['colors'] <- NaN

  for(i in 1:nrow(classes)){
    ID <- classes$ID[i]
    classes$newID[i] = legend$newID[legend$ID==ID]
    classes$colors[i] = legend$colors[legend$ID==ID]
  }
 
  LGN2020 <- NULL
  LGN2020$classes <- classes
  LGN2020$raster <- dataMaps
  LGN2020$legend <- legend
  maps$LGN2020 <- LGN2020
  
  # Gewassen
  # Gewaspath <- paste0(path, '/Gewaspercelen') 
  # dataMaps <- rast(paste0(Gewaspath , '/Gewaspercelen_25m.tif'))
  # classes <- read.dbf(paste0(Gewaspath , '/Gewaspercelen_25m.tif.vat.dbf'), as.is = FALSE)
  # colors <- distinctColorPalette(length(classes[,1]))
  # classes <- cbind(classes, colors)
  # names(classes)[names(classes) == 'Value'] <- 'ID'
  # names(classes)[names(classes) == 'gewas'] <- 'class'
  # rm(colors)
  # Gewassen <- NULL
  # Gewassen$classes <- classes
  # Gewassen$raster <- dataMaps
  # maps$Gewassen <- Gewassen

  # Veendikte
  # MAP IS INCOMPLETE
  Veenpath <- paste0(path, '/Veendikte')
  dataMaps <- rast(paste0(Veenpath , '/Veendikte_50m.tif'))
  dataMaps[dataMaps >50000] <- NA
  classes <- read.dbf(paste0(Veenpath, '/Veendikte_50m.tif.vat.dbf'))
  colors <- distinctColorPalette(length(classes[,1]))
  classes <- cbind(classes, colors)
  rm(colors)
  Veendikte <- NULL
  Veendikte$classes <- classes # value en count als columns
  Veendikte$raster <- dataMaps
  maps$Veendikte <- Veendikte
   
  
  ## Bodemkaart # heeft geen ID - class beschrijving
  Bodempath <- paste0(path, '/Bodemkaart')
  dataMaps <- rast(paste0(Bodempath , '/Bodemkaart_5m.tif'))
  classes <- read.csv(paste0(Bodempath , '/reclassified_soilclasses3.csv'), as.is = FALSE)
  legend <- read.csv(paste0(Bodempath, '/soil_legend_2.csv'), sep=';')
  names(classes)[names(classes) == 'class'] <- 'oldclass'
  names(classes)[names(classes) == 'ID'] <- 'oldID'
  names(classes)[names(classes) == 'newclass'] <- 'class'
  names(classes)[names(classes) == 'newcode'] <- 'ID'
  
  # Wietse's colors:
  # colors <- distinctColorPalette(length(classes[,1]))
  # classes <- cbind(classes, colors)
  # rm(colors)
  
  # set new ID and class-colors in legend
  legend['newID'] <- 1:nrow(legend)
  colorsSOIL <- hcl.colors(15, palette = "Earth")
  legend['colors'] <- col2hex(colorsSOIL)
  
  # add to classes
  classes['newID'] <- NaN; classes['colors'] <- NaN
  
  for(i in 1:nrow(classes)){
    ID <- classes$ID[i]
    classes$newID[i] = legend$newID[legend$ID==ID]
    classes$colors[i] = legend$colors[legend$ID==ID]
  }
  
  Bodemkaart <- NULL
  Bodemkaart$classes <- classes
  Bodemkaart$raster <- dataMaps
  Bodemkaart$legend <- legend
  maps$Bodemkaart <- Bodemkaart
  
  
  
  
  ## Grondwatertrap
  Grwaterpath <- paste0(path, '/Grondwatertrappen/gt2018-QGIS')
  dataMaps <- rast(paste0(Grwaterpath , '/Gt2018_ned.tif'))
  classes <- read.dbf(paste0(Grwaterpath , '/Gt2018_ned.tif.vat.dbf'), as.is = FALSE)
  names(classes)[names(classes) == 'Value'] <- 'ID'
  names(classes)[names(classes) == 'Gt_class'] <- 'class'
  
  # Wietse's colors
  # colors <- distinctColorPalette(length(classes[,1]))
  # classes <- cbind(classes, colors)
  # rm(colors)
  
  # legend even with no reclassification, so it can be used the same way as
  legend <- classes[,c('ID', 'class')]
  colorsGRWT <- hcl.colors(19, palette = "Fall")
  legend['colors'] <- col2hex(colorsGRWT)
  classes['colors'] <- col2hex(colorsGRWT)
  
  
  Grondwatertrap <- NULL
  Grondwatertrap$classes <- classes
  Grondwatertrap$raster <- dataMaps
  Grondwatertrap$legend <- legend
  maps$Grondwatertrap <- Grondwatertrap
  
  ## Drooglegging
  Drglegpath <- paste0(path, '/Drooglegging')
  dataMaps <- rast(paste0(Drglegpath , '/drooglegging.tif'))
  crs(dataMaps) <- 'epsg: 28992'#crs("+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +units=m +no_defs")
  classes <- read.dbf(paste0(Drglegpath , '/drooglegging.tif.vat.dbf'), as.is = FALSE)
  names(classes)[names(classes) == 'Value'] <- 'ID'
  classes$class <- c("0 cm", "< 30 cm", "< 60 cm", "< 90 cm", "> 90 cm")
  colors <- distinctColorPalette(length(classes[,1]))
  classes <- cbind(classes, colors)
  rm(colors)
  Drooglegging <- NULL
  Drooglegging$classes <- classes
  Drooglegging$raster <- dataMaps
  maps$Drooglegging <- Drooglegging

  return(maps)
}


