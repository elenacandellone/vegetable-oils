library(dplyr)
library(vroom)
library(ggplot2)
source("theme.R")

plot_2ABC = function(preprocess = FALSE, oil = "olive") {

	data = readRDS(paste0("processed/fig2ABC_", oil, ".rds"))

	top = 10
	data = data %>%
		filter(remove == 0) %>%
		slice(1:top) %>%
		mutate(id = row_number())

	if(oil == "coconut") {
		col = "#fdb462"
	} else if(oil ==  "olive") {
		col = "#386cb0"
	} else if(oil == "palm") {
		col = "#97CC04"
	}

	p = ggplot(data, aes(y = norm, x = id)) +
		geom_col(fill = col, color = "black") +
		theme_publication() +
		theme(axis.title.y = element_blank(),
			plot.margin=unit(c(5,5,5,2),"mm")) +
		ggtitle(oil) +
		scale_x_continuous(expand = c(0, 0), breaks = data$id, labels = data$hashtag) +
		scale_y_continuous(expand = c(0, 0), limits = c(0, 1.5)) +
		ylab("% of tweets") +
		coord_flip()

}
