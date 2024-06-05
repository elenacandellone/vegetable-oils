library(ggplot2)
library(tidyr)
library(cowplot)
source("theme.R")

plot_4BC = function(data, title) {
	
	Sys.setlocale("LC_TIME", "C")
	
	p = ggplot(data, aes(x = date, y = count, color = sentiment)) + 
		geom_line() +
		geom_point() +
		theme_publication() +
		scale_color_manual(values = c("positive" = "#3fbbc7", "negative" = "#de6666", "neutral" = "#a1a09e"),
					breaks = c("positive", "neutral", "negative")) +
		theme(legend.position = c(0.25, 0.65),
			legend.direction = "vertical",
			legend.background = element_blank(),
			axis.title.x=element_blank(),
			plot.margin=unit(c(5,10,5,2),"mm"),
			legend.text = element_text(size = 12)) +
		ylab("number of tweets") +
		scale_x_date(expand = c(0,0), limits = c(as.Date("2018-01-01"), as.Date("2019-01-01")),
				date_breaks = "2 months", date_labels = "%b %Y") +
		ggtitle(title)

	return(p)
}

plot_4B = function(preprocess = FALSE) {
	data = readRDS("processed/fig4_iucn_biodiversity.rds")

	p = plot_4BC(data, 'IUCN or Biodiversity')
	return(p)
}

plot_4C = function(preprocess = FALSE) {
	data = readRDS("processed/fig4_orangutan_icelandfoods.rds")
	
	p = plot_4BC(data, 'Orangutan or Iceland Foods')
	return(p)
}
