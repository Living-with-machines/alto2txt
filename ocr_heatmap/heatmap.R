#generates a plot of the OCR XML, coloured by word confidence. 
#Requires converting the PDF to JPEG first, in an external editor. Works on output of wordconfidence.py.
#This could probably be done all in Python (matplotlib?) but I only know how to do this bit in R.

require(ggplot2)
require(colorRamps)
require(jpeg)
require(grid)
require(RColorBrewer)

setwd("C:/Users/yryan/Desktop/confidence_heatmap")
#set to the directory you've put the xml and JPEG image


coordinates_confidence = read.csv("coordinates_confidence.txt", header=FALSE)
#opens the file created by wordconfidence.py

img = jpeg::readJPEG("filename.jpg")
#change filename to the name of your image


g = rasterGrob(img, width=unit(1,"npc"), height=unit(1,"npc"),
                interpolate = FALSE)
#creates a raster file of the image - might need some width/height adjustment 
#so that the points sit exactly on the image, but it's close enough

ggplot(coordinates_confidence, aes(V1,V2)) +
  annotation_custom(g, xmin=-Inf, xmax=Inf, ymin=-Inf, ymax=Inf) +
  geom_point(aes(color=V3, alpha = .5)) +
  scale_colour_distiller(type = "seq", palette = "RdYlGn",
                         direction = 1, space = "Lab",
                         na.value = "grey50", guide = "colourbar", aesthetics = "colour") + 
  scale_y_reverse()
#scale needs to be reversed due to the way R plots points. 

#creates the plotted points coloured by word confidence. 
#Play around with alpha and palette (colours from RColorBrewer)
