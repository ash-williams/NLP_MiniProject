import json
from pymongo import MongoClient
import numpy as np
import codecs
import os

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
db = client[config['db_client']]

articles = db.articles
analysis = db.analysis
indicators = db.indicators

#delete CSV if exists
try:
    os.remove('./results.csv')
except:
    print('CSV didnt exist or couldnt be deleted')

min_word_count = config['min_word_count']

count = 0
avg_ind = []
avg_wc = []

# csv titles
csv_str = "Date, Title, Word Count, Indicators, Percentage, URL, "

for indicator in indicators.find():
	csv_str += indicator['name'] + ", "

csv_str += "\n"

for anal in analysis.find({"total_words": {"$gt": min_word_count}}).sort("percentage_wc_totalIncCount", -1):
    article_id = anal['article_id']
    article = articles.find_one({"_id":article_id})

    count = count + 1

    title = article['title']
    date = article['date']
    url = article['url']

    title = title.replace(',', ' ')
    date = date.replace(',', ' ')

    word_count = anal['total_words']
    total_indicators = anal['total_indicator_count']
    percentage = anal['percentage_wc_totalIncCount']

    csv_str += str(date) + ", " + str(title) + ", " + str(word_count) + ", " + str(total_indicators) + ", " + str(percentage) + ", " + str(url) + ", "

    for indicator in indicators.find():
        ind = indicator['name']
        i_percent = anal[ind]['percentage']
        i_percent_to_3 = '{0:.3f}'.format(i_percent)
        csv_str += str(i_percent_to_3) + ", "

    csv_str += "\n"

    avg_ind.append(total_indicators)
    avg_wc.append(word_count)


average_indicators = np.mean(avg_ind)
average_wordcount = np.mean(avg_wc)

with codecs.open("results.csv",'w',encoding='utf8') as f:
    f.write(csv_str)
