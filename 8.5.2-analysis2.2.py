import json
import os
from pymongo import MongoClient
import nltk
from nltk.sem import relextract
import string


# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
db = client[config['db_client']]

articles = db.articles
indicators = db.indicators
analysis = db.analysis
named_ents = db.noun_named_entities

named_ents.drop()

count = 0

named_entities = []

for article in articles.find():
    text = article['article_text']
    url = article['url']
    id = article['_id']
    
    words = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(words)
    
	
    int_count = 0
    words = []
    for item in tagged:
        if item[1] in ['NN', 'NNS', 'NNP', 'NNPS']:
            word = item[0]
            
            word = word.lower()
            
            punctuation_exceptions = ['/', '-']
            for c in string.punctuation:
                #try:
                if c in punctuation_exceptions:
                    word = word.replace(c, " ")
                else:
                    word = word.replace(c,"")
            
            split = word.split(" ")
            for word in split:
                words += [word]
           
            int_count += 1
    
    ne_url = [url] + [words]
    named_entities += [ne_url]

	
    count = count + 1
    print(int_count)
	

print("Generated List")
print(named_entities)
print(count)
print(len(named_entities))




for item in named_entities:
	url = item[0]
	words = item[1]
	
	for word in words:
		doc = named_ents.find_one({"url": url})
		if doc:
			doc_words = doc['words']
			if word in doc_words:
				print("URL and word already exists")
			else:
				#print(doc_words)
				#print(word)
				new_words = doc_words + [word]
				
				named_ents.update({"url": url }, {"$set": {
				 	"words": new_words,
				}})	
		
		else:
			json = {
						"url": url,
						"words": [word]
					}
			#print(json)
			named_ents.insert_one(json)
	
