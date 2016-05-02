import json
import os
from pymongo import MongoClient
import nltk
from nltk.sem import relextract


# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
db = client[config['db_client']]

named_ents = db.noun_named_entities
word_list = db.noun_word_list

word_list.drop()

count = 0

word_urls = []

for ne in named_ents.find():
    url = ne['url']
    words = ne['words']
    for word in words:
        try:
            try:
                word = word.lower()
            except:
                word = word[0].lower()
                
            doc = word_list.find_one({"word": word})
            if doc:
                doc_urls = doc['urls']
                if url in doc_urls:
                    print("URL and word already exists")
                else:
                    #print(doc_words)
                    #print(word)
                    new_urls = doc_urls + [url]
                
                    word_list.update({"word": word }, {"$set": {
                    "urls": new_urls,
                    }})	
                
            else:
                json = {
                    "word": word,
                    "urls": [url]
                }
                #print(json)
                word_list.insert_one(json)
        except:
            print(word)
	
	count = count + 1
	print(count)
	
print("Final Count")
print(count)




	
