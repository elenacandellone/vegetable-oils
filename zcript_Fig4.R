library(cowplot)
source("zcript_4A.R")
source("zcript_4BC.R")

pA = plot_4A(TRUE)
pB = plot_4B(TRUE)
pC = plot_4C(TRUE)

lbl_size = 16
top_row = plot_grid(pA, labels = c('a'), label_size = lbl_size, ncol = 1)
bot_row = plot_grid(pB, pC, labels = c('b', 'c'), label_size = lbl_size, ncol = 2)

pdf("plots/Figure4.pdf", width = 12, height = 7)
plot_grid(top_row, bot_row, ncol = 1, rel_heights = c(.4, .6))
dev.off()

