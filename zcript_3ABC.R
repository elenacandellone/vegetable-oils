library(ggplot2)
library(dplyr)
library(cowplot)
source("theme.R")

plot_A = function(oil, title) {
	data = readRDS(paste0("processed/fig3ABC_", oil, ".rds"))
	
	p = ggplot(data, aes(x = time, y = count, color = sentiment)) + 
		geom_line() +
		theme_publication() +
		scale_color_manual(values = c("positive" = "#ce3332", "negative" = "#236b7c", "neutral" = "#FFBA49"),
					breaks = c("positive", "neutral", "negative")) +
		theme(legend.position = c(0.25, 0.85),
			legend.direction = "horizontal",
			legend.background = element_blank(),
			axis.title.x=element_blank()) +
		ylab("monthly tweets") +
		scale_y_continuous(expand = c(0,0), label = scientific_10) +
		scale_x_date(limits = c(as.Date("2006-01-01"), as.Date("2022-01-01")),
				breaks = as.Date(paste0(seq(2006, 2022, by = 2), "-01-01")),
				labels = c("2006", "", "2010", "", "2014", "", "2018", "", "2022")) +
		coord_cartesian(ylim = c(0, 1e5))

	return(p)
}

plot_3ABC = function(lbl_size) {

	pA = plot_A('coconut', "coconut oil")
	pB = plot_A('olive', "olive oil")
	pC = plot_A('palm', "palm oil")
	
	legend = get_legend(pA + 
			theme(legend.position = "top", 
				legend.key.size = unit(2, "cm"), 
				legend.text = element_text(size = 16),
				legend.margin = margin(0, 0, 1, 0, unit = "cm"),
				legend.key = element_blank()) + 
			guides(color = guide_legend(override.aes = list(size = 1)))
		) 
	pA2 = pA + theme(legend.position = "none")
	pB2 = pB + theme(legend.position = "none")
	pC2 = pC + theme(legend.position = "none")

	top_row = plot_grid(pA2, pB2, pC2, labels = c('d', 'e', 'f'), label_size = lbl_size, ncol = 3)
	top_row = plot_grid(legend, top_row, nrow = 2, rel_heights = c(.1, .9))

	return(top_row)
}
