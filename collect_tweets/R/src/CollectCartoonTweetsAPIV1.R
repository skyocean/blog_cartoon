# Clean the console
rm(list = ls())

#Set working directory
setwd("D:/blog/code/project cartoon/collect-tweets/R/sample output")

# Load libraries

library("rtweet")
library("jsonlite")

#I still like to remove scientific notation
options(scipen = 99)

# Access twitter api 1

# Replace your tokens here 
setup_twitter_oauth(consumer_key = 'xxx',
                    consumer_secret = 'xxx',
                    access_token = 'xxxx', 
                    access_secret = 'xxxx')
#Specify the query for collecting tweets
query <- "(Totoro OR Walle OR\"Wall E\") -filter:retweets -filer:replies -filter:quote filter:verified"

#Get tweets data 
tweets<- search_tweets2(query, lang ="en", n = Inf, retryonratelimit = TRUE)

#You can also search users 
#Specify the query for collecting users
#queryu <- "totoro filter:verified"

#Get tweets data 
#tweets <- search_users(queryu, n = 1000, parse = T)

#Parse the data
tweetsclean <- subset(tweets, select = c(query, user_id, status_id, created_at, screen_name, text, source, display_text_width, hashtags, retweet_count, favorite_count, mentions_screen_name, verified))

#Unlist the hashtages and metions and put them in the final dataset
tweetsclean$hashtags <- vapply(tweetsclean$hashtags, paste, collapse = ", ", character(1L))
tweetsclean$mentions_screen_name <- vapply(tweetsclean$mentions_screen_name, paste, collapse = ", ", character(1L))

#Save the dataset
write.csv(tweetsclean, "xxx.csv", row.names = F, fileEncoding = "UTF-8")
