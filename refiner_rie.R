
library(refineR)
library(dplyr)


refineR <- function(data){
  data <- read.csv(file="pathways_results.csv", sep =",", header = F)
  data <- data %>%
    mutate(across(where(is.numeric), ~ ./sum(.)))
  data <- as.matrix(data)
  data_RI <- findRI(Data = data)
  print(data_RI)
  getRI(data_RI)
  png("Rplots.png")
  plot(data_RI,  showPathol = TRUE, title = "Estimated Reference Interval")
  dev.off()
}


results <- c(refineR(data))

