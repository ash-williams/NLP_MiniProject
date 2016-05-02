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

nn_wl = db.noun_word_list.find()
st_wl = db.stanford_word_list.find()
ne_wl = db.word_list.find()

fn_wl = db.final_word_list.find()

db.final_word_list.drop()

count = 0
duplicate = 0

def insert_into_final(item):
    global count
    global duplicate
    word = item['word']
    urls = item['urls']
    exists = db.final_word_list.find_one({"word": word})
    if not exists:
        json = {
            "word": word,
            "urls": urls
        }
        db.final_word_list.insert_one(json)
        count += 1
        print("Count: " + str(count))
    else:
        existing_urls = exists['urls']
        
        for url in urls:
            if url in existing_urls:
                print("Nothing to do")
            else:
                new_urls = existing_urls + [url]
                
                db.final_word_list.update({"word": word}, {"$set": {
                    "urls": new_urls,
                }})
        
        duplicate += 1
        print("Duplicates: " + str(duplicate))
        
for item in nn_wl:
    insert_into_final(item)

for item in st_wl:
    insert_into_final(item)
    
for item in ne_wl:
    insert_into_final(item)
  
print("Final:")  
print("Count: " + str(count))
print("Duplicates: " + str(duplicate))
        