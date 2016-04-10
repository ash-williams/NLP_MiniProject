from pymongo import MongoClient
import json

#Connect to mongo
client = MongoClient('mongodb://localhost/27017')
db = client['uc-proto']
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
		ind_json = {indicator['name']: ind_count}
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
	
