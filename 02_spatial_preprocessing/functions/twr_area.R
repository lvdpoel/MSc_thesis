#---------------------
# make tower location and area into rasters
#-----------------------

twr_area <- function(lat, lon, margin){
  # prepare tower location 
  m <- matrix(c(lon, lat), nrow = 1, ncol = 2)
  twr_latlon <- vect(m, type='points')
  crs(twr_latlon) <- 'epsg:4326'
  twr <- project(twr_latlon, 'epsg:28992')

  plot_area <- rast()
  ext(plot_area) <-  c(ext(twr)[1] - margin, ext(twr)[1] +margin, ext(twr)[3]-margin, ext(twr)[3]+margin)
  crs(plot_area)<-'epsg:28992'

  return(list(TowerLocation=twr, PlotArea=plot_area))
}


