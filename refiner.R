
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
  plot(data_RI,  showPathol = TRUE, title = "Estimated Reference Interval")
  dev.copy(png,'Rplots.png')
  dev.off()
}


id <- read.csv(file="id_results.csv", sep =",", header = F)
z <- id[,1]
sample <- function(z){
  
  capture <- capture.output(refineR())
  x <- capture[4]
  x <- substr(x, 27,37)
  x <- as.numeric(x)
  y <- capture[5]
  y <- substr(y, 27,37)
  y <- as.numeric(y)
  q <- between(z, x, y)
  w <- if(q == FALSE){
    print("The sample is not in estimated reference interval")
  } else {
    print("The sample is in estimated reference interval")
  }
}

results <- c(sample(z))

