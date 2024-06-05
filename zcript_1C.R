library(ggplot2)
library(dplyr)
source("theme.R")

plot_1C = function(preprocess = FALSE) {

	data = readRDS("processed/fig1C_oils.rds")
	words = readRDS("processed/fig1C_words.rds")
	
	p = ggplot() + 
		geom_line(data = words, aes(x = time, y = mean, color = "common words"), size = .2) +	
		geom_point(data = words, aes(x = time, y = mean, color = "common words")) +
		geom_errorbar(data = words, aes(x = time, ymin = mean-sd, ymax = mean+sd), width = .2) +	
		geom_line(data = data, aes(x = time, y = growth, color = oil), size = .2) +
		geom_point(data = data, aes(x = time, y = growth, color = oil)) +
		theme_publication() +
		scale_color_manual(values = c("coconut" = "#fdb462", "olive" = "#386cb0", "palm" = "#97CC04", "common words" = "#662506")) +
		theme(legend.position = c(0.25, 0.85),
			legend.direction = "vertical",
			legend.background = element_blank(),
			axis.title.x=element_blank()) +
		ylab("growth relative to 2007") +
		scale_y_continuous(expand = c(0,0), label = scientific_10, limits = c(0, 2.1e4)) +
		scale_x_continuous(breaks = seq(2008, 2022, by = 2), labels = c("", "2010", "", "2014", "", "2018", "", "2022"), limits=c(2008, 2022))

	return(p)
}
