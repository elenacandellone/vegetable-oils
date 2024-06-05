library(cowplot)

lbl_size = 16
source("zcript_3ABC.R")
top_row = plot_3ABC(lbl_size)
source("zcript_3DEF.R")
bot_row = plot_3pie(lbl_size)

pdf("plots/Figure3.pdf", width = 12, height = 6)
plot_grid(bot_row, top_row, ncol = 1, rel_heights = c(.5, .5))
dev.off()
