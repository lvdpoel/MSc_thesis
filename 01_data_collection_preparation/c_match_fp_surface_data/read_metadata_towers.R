# read metadata towers
rm(list=ls())

lw <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/eddypro_20210617_20210708_MOB_02_EC_LangeweideHoog_metadata_2022-01-27T001342_adv.csv")
head(lw)
names(lw)
lw[,'master_sonic_height'] # 5.7

zv <- read.csv("C:/Users/l_vdp/Documents/MSc_Thesis/data/preprocessing/towers/eddypro_20210528_20210713_Zegveld_metadata_2021-08-13T100934_adv.csv")
head(zv)
zv[,'master_sonic_height'] # eerste 600 op 3.40, daarna naar 3.95
dim(zv)

