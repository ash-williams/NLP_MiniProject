import json
from pymongo import MongoClient

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient(config['db_url'])
db = client[config['db_client']]

articles = db.articles
indicators = db.indicators
analysis = db.analysis

count = 0

#drop analysis table - refresh each time script is run
analysis.drop()

for article in articles.find():
	text = article['article_no_punctuation_and_lower']
	url = article['url']
	id = article['_id']
	
	#try:

		# for each indicator
		# take a count of occurances
		# store them in an analysis collection
	data = {
		"article_id": id,
		"url": url
	}
	
	words = text.split(' ')
	word_count = len(words)
	data.update({"total_words":word_count})
	
	total_indicator_count = 0
	
	for indicator in indicators.find():
		ind_count = text.count(" " + indicator['name'] + " ")
		total_indicator_count += ind_count
		ind_percentage = (100 * ind_count)/word_count
		ind_json = {indicator['name']: {"count": ind_count, "percentage": ind_percentage}}
		data.update(ind_json)
	
	data.update({"total_indicator_count": total_indicator_count})
	
	percentage = (100 * total_indicator_count)/word_count
	
	data.update({"percentage_wc_totalIncCount": percentage})
	
	print(data)
	analysis.insert_one(data)
	
	count = count + 1
	
	#except:
	#	print("Error")

print(count)
	
