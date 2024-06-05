library(ggplot2)
library(dplyr)
source("theme.R")

plot_1A = function(preprocess = FALSE) {

	data = readRDS("processed/fig1A_oils.rds")
	
	p = ggplot(data, aes(x = time, y = cumulative, color = oil)) + 
		geom_line() +
		theme_publication() +
		scale_color_publication() +
		theme(legend.position = c(0.25, 0.65),
			legend.direction = "vertical",
			legend.background = element_blank(),
			axis.title.x=element_blank()) +
		ylab("cumulative tweets") +
		scale_y_continuous(expand = c(0,0), label = scientific_10, limits = c(0, 8e6)) +
		scale_x_date(limits = c(as.Date("2006-01-01"), as.Date("2022-01-01")),
				breaks = as.Date(paste0(seq(2006, 2022, by = 2), "-01-01")),
				labels = c("2006", "", "2010", "", "2014", "", "2018", "", "2022"))

	return(p)
}
