library(ggplot2)
library(dplyr)
library(RColorBrewer)
source("theme.R")

plot_1D = function(preprocess = FALSE) {

	data = readRDS("processed/fig1D_map.rds")
	data = data %>% filter(region != "Antarctica")
	
	p = ggplot(data, aes(long, lat, fill = count, group = group)) + 
		geom_polygon(color = "#e4e6e3", size = 0.01) +
		theme_publication() +
		theme(legend.position = "right",
			legend.direction = "vertical",
			legend.background = element_blank(),
			axis.title.x = element_blank(),
			axis.title.y = element_blank(),			
			axis.ticks = element_blank(),
			axis.line = element_blank(),
			axis.text = element_blank()) +
		 scale_fill_gradientn(name = "palm oil\ntweets", colours=brewer.pal(9,"Greens"),
		 	limits = c(0, 10000)) +
		 guides(fill = guide_colorbar(title.position="top", 
			title.hjust = 0,
			ticks.colour = "black",
			ticks.linewidth = 2,
			label.theme = element_text(size=15),
			title.theme = element_text(size=16),
			frame.colour = "black",
			frame.linewidth = 1,
			barheight = unit(.5,"npc"),
			barwidth = unit(.02,"npc")))

	return(p)
}
