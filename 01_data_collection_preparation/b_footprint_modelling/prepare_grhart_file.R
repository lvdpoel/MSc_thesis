"""

This script prepares the airborne-measurements file so it can be used
with Kljun functions. Column names are changed and planetary boundary layer
height is added as a column.

---
Input:
raw airborne measurements file (.csv)

---
Output:
airborne measurement file, ready to use with Kljun (.csv)


"""


## Cleanup
rm(list = ls(all.names = TRUE))

# Get data
file_in = 'C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/grhart_allL.csv'
dataColnames <- read.csv(file_in, skip = 5,nrows = 1) # needs to be checked for new files
data <- read.csv(file_in, skip = 6) %>% data.frame() # same here
colnames(data)<-colnames(dataColnames)
df <- data.frame(data) 


# Give correct names for Kljun script
df <- df %>% 
  rename(
    zm = Height,
    umean = WindSpd,
    ol = L,
    ustar = Ustar,
    sigmav = Std_V,
    wind_dir = WindDir
  )


# Calculation planetary boundary layer height (PBLH) (h in calc_footprint_FFP_climatology)
latitude = data$Lat * (pi / 180)        # degrees -> radians
angular_velocity = 7.2921159 * 10^-5     # rad/s
coriolis_parameter = 2 * angular_velocity * sin(latitude)
c_n = 0.3  
PBLH = c_n * df$ustar / coriolis_parameter
df['h'] <- PBLH

# drop CH4 and CH4flx
df <- subset(df, select = -c(CH4,CH4flx,Tdew))

# Save to csv
file_out = 'C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/airborne_footprints/fp_meas_grhart.csv'
write.csv(df, file_out, row.names = FALSE)

 


