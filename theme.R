scientific_10 = function(x) {
  library(scales)
  parse(text=ifelse(x < 1e-8, "0", gsub("e\\+", "%*%10^", scales::label_scientific()(x))))
}

theme_publication <- function(base_size=14) {
      library(grid)
      library(ggthemes)
      (theme_foundation(base_size=base_size)
       + theme(plot.title = element_text(face = "bold",
                                         size = rel(1.2), hjust = 0.5),
               text = element_text(family = "Helvetica"),
               panel.background = element_rect(colour = NA),
               plot.background = element_rect(colour = NA),
               panel.border = element_rect(colour = NA),
               axis.title = element_text(face = "bold",size = rel(1)),
               axis.title.y = element_text(angle=90,vjust =2),
               axis.title.x = element_text(vjust = -0.2),
               axis.text = element_text(), 
               axis.line = element_line(colour="black", size = .2),
               axis.ticks = element_line(, size = .2),
               panel.grid.major = element_blank(), #element_line(colour="#f0f0f0"),
               panel.grid.minor = element_blank(),
               legend.key = element_rect(colour = NA),
               legend.position = "bottom",
               legend.direction = "horizontal",
               legend.key.size= unit(0.3, "cm"),
               #legend.margin = unit(0, "cm"),
               #legend.title = element_text(face="italic"),
               legend.title = element_blank(),
               plot.margin=unit(c(5,2,5,2),"mm"),
               strip.background=element_rect(colour="#f0f0f0",fill="#f0f0f0"),
               strip.text = element_text(face="bold")
          ))
      
}

scale_fill_publication <- function(...){
      library(scales)
      discrete_scale("fill","publication",manual_pal(values = c("#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99","#984ea3","#ffff33","#97CC04")), ...)

}

scale_color_publication <- function(...){
      library(scales)
      discrete_scale("colour","publication",manual_pal(values = c("#662506","#fdb462","#7fc97f","#ef3b2c","#386cb0","#97CC04","#fb9a99","#984ea3","#ffff33","#a6cee3")), ...)

}
