import json
import os
from pymongo import MongoClient
import nltk
from nltk.tag import StanfordNERTagger
import string

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
db = client[config['db_client']]

st = StanfordNERTagger("classifiers/english.conll.4class.distsim.crf.ser.gz", "classifiers/stanford-ner.jar")#"/usr/share/stanford-ner/classifiers/all.3class.distsim.crf.ser.gz", "/usr/share/stanford-ner/stanford-ner.jar")

articles = db.articles
indicators = db.indicators
analysis = db.analysis
stanford_named_ents = db.stanford_named_entities

# stanford_named_ents.drop()

count = 0

named_entities = []


for article in articles.find():
    text = article['article_text']
    url = article['url']
    id = article['_id']
	
    if not (stanford_named_ents.find_one({"url": url})):
        print("New Link")
        tagged = st.tag(text.split())
        words = []
        
        for word in tagged:
            #print(word[1])
            if word[1] != 'O':
                if word[0] not in words:
                    word = word[0]
                    punctuation_exceptions = ['/', '-']
                    for c in string.punctuation:
                        #try:
                        if c in punctuation_exceptions:
                            word = word.replace(c, " ")
                        else:
                            word = word.replace(c,"")
                    
                words += [word]
        
        #print(words)
        # ne_url = [url] + [words]
        # named_entities += [ne_url]
        for word in words:
    		doc = stanford_named_ents.find_one({"url": url})
    		if doc:
    			doc_words = doc['words']
    			if word in doc_words:
    				print("URL and word already exists")
    			else:
    				#print(doc_words)
    				#print(word)
    				new_words = doc_words + [word]
    				
    				stanford_named_ents.update({"url": url }, {"$set": {
    				 	"words": new_words,
    				}})	
    		
    		else:
    			json = {
    						"url": url,
    						"words": [word]
    					}
    			#print(json)
    			stanford_named_ents.insert_one(json)
        
        
    count = count + 1
    print(count)

#print(named_entities)
    
# for item in named_entities:
# 	url = item[0]
# 	words = item[1]
	
# 	for word in words:
# 		doc = stanford_named_ents.find_one({"url": url})
# 		if doc:
# 			doc_words = doc['words']
# 			if word in doc_words:
# 				print("URL and word already exists")
# 			else:
# 				#print(doc_words)
# 				#print(word)
# 				new_words = doc_words + [word]
				
# 				stanford_named_ents.update({"url": url }, {"$set": {
# 				 	"words": new_words,
# 				}})	
		
# 		else:
# 			json = {
# 						"url": url,
# 						"words": [word]
# 					}
# 			#print(json)
# 			stanford_named_ents.insert_one(json)