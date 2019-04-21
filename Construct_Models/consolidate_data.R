#this reads in RYANDATA - raw from webscraper and cleans up categories
library(plyr)

data <- read.csv('RYANDATA.csv', stringsAsFactors = F)
colnames(data)
colnames(data) <- c('X', 'topic', 'authors', 'title', 'journal', 'year', 'vol_issue', 'doi')

data.complete <- data[(complete.cases(data$topic)),]
nrow(data.complete)
table(data.complete$topic)
unique(data.complete$topic)


#Remove Unique Topic
data.complete$topic[grepl('UNIQUE',data.complete$topic)] <- NA
data.complete <- data.complete[(complete.cases(data.complete$topic)),]
table(data.complete$topic)
nrow(data.complete)

#rename long names
data.complete$topic[grepl('CARDIO',data.complete$topic)] <- 'CARDIOVASCULAR'
data.complete$topic[grepl('CELL',data.complete$topic)] <- 'CELLULAR'
data.complete$topic[grepl('HAND',data.complete$topic)] <- 'HAND/FOOT'
data.complete$topic[grepl('TRAUMA',data.complete$topic)] <- 'TRAUMA/IMPACT'
data.complete$topic[grepl('VISUAL',data.complete$topic)] <- 'VISUAL/VESTIBULAR'

data.complete <- data.complete[(complete.cases(data.complete$topic)),]
table(data.complete$topic)
nrow(data.complete)


# consolidate data ----
#save csv of changes above
write.csv(data.complete, file = 'RYANDATA_consolidated.csv')

