calc_ruimt_data_in_fp <- function(data=maps$LGN2020, fpraster=fp, cat=T){
#--------------------------------
# Function to calculate contributions of 'ruimtelijke data veenweiden' maps. 
#
# Input: data: should be of type as provided by importMaps function, i.e. with raster, classes, and legend.
# fpraster: raster of footprint to be calculated, cat: logical. If True: categorical data: function
# calculates contribution of every class. if False, for continuous data, function calculates average
#
# Output: dataframe with contributions, to be added to dataframe with measurements
#------------------------------------------
  
  # get variables of data
  map <- data$raster
  qty <- names(map)
  classes <- data$classes
  legend <- data$legend
  
  # project fp to crs of map
  fp <- project(fpraster, crs(map)) # duurt 4 sec
  fp[is.na(fp)] <- 0
  fp[fp<0] <- 0
  
  # crop map file to fp file size
  map.1 <- crop(map, fp, snap='out')
  
  #plot(map.1, type='classes', levels=legend$class, legend=TRUE, main ='LGN2020')
  
  # for reclassification
  classes['newID'] <- NaN
  
  # for reclassification purposes:
  if('oldID' %in% colnames(classes)){
    
    # save new ID's in classes
    for(i in 1:nrow(classes)){
      ID <- classes$ID[i]
      classes$newID[i] = legend$newID[legend$ID==ID]
    }
    
    # reclassification matrix
    rcl <- matrix(c(classes$oldID, classes$newID), ncol=2, nrow=nrow(classes))
    map.2 <-classify(map.1, rcl) ## aangepast 
    levels(map.2) <- legend$newID
    
  } else {map.2 <- map.1}
  
  # makes fp resolution equal to map.1 resolution
  fp.final <- resample(fp, map.2,method = "near")  
  
  # put cell-values in dataframe, for both footprint and map 
  fp.df <- as.data.frame(fp.final * prod(res(fp.final)), na.rm=F)
  map.df <- as.data.frame(as.matrix(map.2)[,1])
  df <- cbind(fp.df, map.df) %>% na.omit()
  colnames(df) <- c('fp', 'newID')
  
  
  if(cat == T){ # means it's categorical data
    contr_df <- data.frame(matrix(ncol = nrow(legend), nrow = 1)) 
    colnames(contr_df) <- legend$newID
    
    # for every class, calculate summed contribution
    for(j in 1:nrow(legend)){
      newID <- legend$newID[j]
      perc_in_fp <- sum(df$fp[df$newID == newID])
      contr_df[1,newID] <- perc_in_fp / sum(fp.df, na.rm = T) # to make entire fp equal to 100%
    } 
    
    colnames(contr_df) <- legend$ID

  } else{ # for continuous data
    df['x'] <- df$fp * df$ID
    data_contr <- sum(df$x) / sum(fp.df, na.rm = T) # to make entire fp equal to 100%
    contr_df <- data.frame(qty = data_contr)
  }
  
  return(contr_df)
}



