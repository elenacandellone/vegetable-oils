library(ggplot2)
library(dplyr)
source("theme.R")

plot_4A = function(preprocess = TRUE) {	
	Sys.setlocale("LC_TIME", "C")

	data = readRDS("processed/fig4A_evolution.rds")
	
	p = ggplot(data, aes(x = date, y = count, color = label)) + 
		geom_line() +
		geom_point() +
		theme_publication() +
		scale_color_manual(values=c("#f2b3e9", "#a17dd3", "#80bcef", "#2f6fcc")) +
		theme(legend.position = c(0.25, 0.65),
			legend.direction = "vertical",
			legend.background = element_blank(),
			axis.title.x=element_blank(),
			plot.margin=unit(c(5,10,5,2),"mm"),
			legend.text = element_text(size = 12)) +
		ylab("number of tweets") +
		scale_y_continuous(expand = c(0,0), limits = c(0, 25000)) +
		scale_x_date(expand = c(0,0), limits = c(as.Date("2018-01-01"), as.Date("2019-01-01")),
				date_breaks = "2 months", date_labels = "%b %Y")

	return(p)
}
