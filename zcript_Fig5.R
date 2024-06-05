library(ggplot2)
library(ggrepel)
library(dplyr)
library(patchwork)
source("theme.R")

plot_pie = function(area) {

	data_sentiment = readRDS("processed/fig5_sentiment.rds")

	a = data_sentiment %>% 
		filter(type == area) %>%
		group_by(sentiment) %>%
		summarize(count = sum(count))

	a = a %>% ungroup() %>%
		mutate(count = count / sum(count)) %>%
		mutate(text = paste0(sprintf("%.0f", count * 100), "%"))

	a$ymax = cumsum(a$count)
	a$ymin = c(0, head(a$ymax, n=-1))
	a$labelPosition = (a$ymax + a$ymin) / 2

	pB = ggplot(a, aes(x = "", y = count, fill = sentiment)) +
		geom_bar(stat = "identity", width = 1) +
		theme_publication() +	
		coord_polar("y", start = 0) +
		theme_void() +
		xlab(area) +
		theme(legend.position="none",
			axis.title.y = element_text(color = "gray", size=18, face="bold")) +
		scale_fill_manual(values = c("positive" = "#ce3332", "negative" = "#236b7c", "neutral" = "#FFBA49")) 

	print(area)
	return(pB)
}


data = readRDS("processed/fig5_virality.rds")
fake = data.frame(x = c(1, 1, 1),  color = c("positive", "neutral", "negative"))

p = ggplot() +
        geom_hline(aes(yintercept = 2), color = "gray", linetype = "dashed") +
        geom_hline(aes(yintercept = 3), color = "gray", linetype = "dashed") +
        geom_vline(aes(xintercept = 2), color = "gray", linetype = "dashed") +
        geom_vline(aes(xintercept = 3), color = "gray", linetype = "dashed") +
	geom_point(data = data, aes(x = IET, y = CS, color = oil, shape = oil), size = 2) +
	geom_errorbar(data = data, aes(x = IET, y = CS, ymin = CS - CS_err, ymax = CS + CS_err, color = oil)) +
	geom_errorbarh(data = data, aes(x = IET, xmin = IET - IET_err, xmax = IET + IET_err, y = CS, color = oil)) +
        geom_bar(data = fake, aes(x = x, fill = color)) +
	scale_color_manual(values = c("coconut" = "#fdb462", "olive" = "#386cb0", "palm" = "#97CC04")) +
	scale_fill_manual(values = c("positive" = "#ce3332", "negative" = "#236b7c", "neutral" = "#FFBA49")) +
	theme_publication() +
	theme(legend.position = c(0.83, 0.12),
		legend.direction = "horizontal",
		legend.key.size = unit(0.5, "cm"),
		axis.title = element_text(size = 22),
		legend.spacing.y = unit(-0.1, "cm")) +
	scale_x_continuous(expand = c(0, 0), limits = c(1, 4)) +
	scale_y_continuous(expand = c(0, 0), limits = c(1, 5.2)) +
	guides(color = guide_legend(override.aes = list(size = 6, linetype = 0))) +
	geom_text_repel(data = data, aes(x = IET, y = CS, label = hashtag)) +
	xlab(expression(paste(alpha[IET]))) +
	ylab(expression(paste(alpha[CS])))


# PIEs

pI = plot_pie("I")
pII = plot_pie("II")
pIII = plot_pie("III")
pIV = plot_pie("IV")
pV = plot_pie("V")
pVI = plot_pie("VI")


# Insets

p = p + inset_element(pI, 0.0, .3, .15, .45)
p = p + inset_element(pII, .27, .25, .52, .4)
p = p + inset_element(pIII, .65, .27, .8, .42)
p = p + inset_element(pIV, .0, .65, .15, .8)
p = p + inset_element(pV, .32, .8, .47, .95)
p = p + inset_element(pVI, .75, .55, .9, .7)


pdf("plots/Figure5.pdf", width = 10, height = 6)
plot(p)
dev.off()


