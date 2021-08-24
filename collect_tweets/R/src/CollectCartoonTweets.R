#clean the console
rm(list = ls())

#set working directory
setwd("D:/blog/code/project cartoon/collect-tweets/R/sample output")

# load library
library("academictwitteR")
library("tibble")

#remove scientific notation
options(scipen = 99)

# Set your own bearer token (replace the XXXXX with your own bearer token)
bearer_token <- "XXXXX"


# Specify the start time in UTC of the time interval when targeted tweets were posted
start_time <- "2018-01-01T00:00:00Z"

# Specify the end time in UTC of the time interval when targeted tweets were posted
end_time <- "2021-08-01T00:00:00Z"

# Specify our query
query <- "(Totoro OR Walle OR \"Wall-E\") lang:en is:verified -is:retweet -is:reply -is:quote"

# pull out the tweets
tweets <- get_all_tweets(query, # this is the place you pass your query
                         start_time, #start time
                         end_time, #end time
                         bearer_token,
                         data_path = "tweetdata", # set up your folder for storing json files
                         bind_tweets = F, # If we set to False, the result will not be bound in the local memory
                         n = 1000000) # set how many tweets you may collect

# Bind results
# a nice dataframe for storing tweets results
tweettidy <- bind_tweets(data_path = "tweetdata", output_format = "tidy")

# There are some extra data of tweets and users, which we would like to put into the final results.
# Thus we bind these raw data together.
tweetraw <- bind_tweets(data_path = "tweetdata") %>% as_tibble
tweetuser <- bind_tweets(data_path = "tweetdata", user = T) %>% as_tibble

# Let us extract hashtags and put into tweettidy set
tweettidy$hashtags <- vapply(tweetraw$entities$hashtags, 
                            function(.x) {paste(.x$tag, collapse = ', ') }, 
                            FUN.VALUE = character(1))

write.csv(tweettidy,"cartoontweetsR.csv", row.names = F, fileEncoding = "UTF-8")
