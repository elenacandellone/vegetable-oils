library(ggplot2)
library(dplyr)
library(cowplot)
source("theme.R")

plot_pie = function(title) {
	data = readRDS(paste0("processed/fig3DEF_", title, ".rds"))
	
	p = ggplot(data, aes(ymax=ymax, ymin=ymin, xmax=4, xmin=3, fill=sentiment)) + 
		geom_rect() +
		geom_text(x = 3.5, aes(y = labelPosition, label = label), size = 6, color = "white", fontface = "bold") +
		theme_publication() +
		scale_fill_manual(values = c("positive" = "#ce3332", "negative" = "#236b7c", "neutral" = "#FFBA49")) +
		coord_polar(theta = "y") +
		theme_void() +
		theme(legend.position = "none",
			text = element_text(family = "Helvetica")) +
		xlim(c(2, 4)) +               
		annotate('text', x = 2, y = 0.5, label = paste0("bold(", title, ")"), size = 7.5, parse = TRUE)

	return(p)
}

plot_3pie = function(lbl_size) {

	pA = plot_pie('coconut')
	pB = plot_pie('olive')
	pC = plot_pie('palm')

	top_row = plot_grid(pA, pB, pC, labels = c('a', 'b', 'c'), label_size = lbl_size, ncol = 3)

	return(top_row)
}
