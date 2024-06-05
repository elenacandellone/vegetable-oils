library(dplyr)
library(vroom)
library(ggplot2)
library(ggpubr)
library(cowplot)
source("theme.R")

plot_2D = function() {
	data = readRDS("processed/fig2D_sample.rds")

	# densities
	xplot = ggplot(data, aes(topic_1, fill = labels)) +
			geom_density(size = 0.1) +
			scale_fill_manual(values = c("coconut" = "#fdb462", "olive" = "#386cb0", "palm" = "#97CC04")) +
			theme_publication() +
			clean_theme() +
			theme(legend.position = "none",
				plot.margin=unit(c(0,0,0,0),"mm"),
				plot.background = element_blank()) +
			scale_y_continuous(expand = c(0, 0))


	yplot = ggplot(data, aes(topic_2, fill = labels)) +
			geom_density(size = 0.1, adjust = 4) +
			scale_fill_manual(values = c("coconut" = "#fdb462", "olive" = "#386cb0", "palm" = "#97CC04")) +
			theme_publication() +
			rotate() +
			clean_theme() +
			theme(legend.position = "none",
				plot.margin=unit(c(0,0,0,0),"mm"),
				plot.background = element_blank()) +
			scale_y_continuous(expand = c(0, 0))

	# scatter
	data = data[sample(1:nrow(data), 10000),]

	points = ggscatter(data, x = "topic_1", y = "topic_2",
		color = "labels", size = 1, alpha = 0.6, shape = 16,
		palette = c("coconut" = "#fdb462", "olive" = "#386cb0", "palm" = "#97CC04"))	 +		
			theme_publication() +
			theme(legend.position = c(0.8, 0.8),
				legend.direction = "vertical",
				plot.margin=unit(c(-10,-20,5,5),"mm")) +
			xlab("topic 1") +
			ylab("topic 2") +
			scale_x_continuous(limits = c(0, 0.8)) +
			scale_y_continuous(limits = c(-0.6, 0.8)) +
			guides(color = guide_legend(override.aes = list(size=4))) 

	# join
	p = ggarrange(xplot, NULL, NULL, NULL, NULL, NULL, points, NULL, yplot,
			ncol = 3, nrow = 3, align = "hv",
			widths = c(2, -0.4, 1), heights = c(1, -0.4, 2))

	return(p)
}


