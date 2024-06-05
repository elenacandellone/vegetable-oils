library(cowplot)
source("zcript_1A.R")
source("zcript_1B.R")
source("zcript_1C.R")
source("zcript_1D.R")

pA = plot_1A()
pB = plot_1B()
pC = plot_1C()
pD = plot_1D()

lbl_size = 16
top_row = plot_grid(pA, pB, pC, labels = c('a', 'b', 'c'), label_size = lbl_size, ncol = 3)

pdf("plots/Figure1.pdf", width = 12, height = 8)
plot_grid(top_row, pD, labels = c('', 'd'), label_size = lbl_size, ncol = 1, rel_heights = c(.4, .6))
dev.off()
