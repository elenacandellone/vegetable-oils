library(cowplot)
source("zcript_2ABC.R")
source("zcript_2D.R")

pA = plot_2ABC(TRUE, "coconut")
pB = plot_2ABC(TRUE, "olive")
pC = plot_2ABC(TRUE, "palm")

pD = plot_2D()
pE = ggplot() + theme_void()

lbl_size = 16
top_row = plot_grid(pA, pB, pC, labels = c('a', 'b', 'c'), label_size = lbl_size, ncol = 3)
bot_row = plot_grid(pD, pE, labels = c('d', 'e'), label_size = lbl_size, ncol = 2)

pdf("plots/Figure2.pdf", width = 12, height = 8)
plot_grid(top_row, bot_row, ncol = 1)
dev.off()
