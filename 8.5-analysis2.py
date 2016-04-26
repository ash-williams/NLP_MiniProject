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


def extract_entities(text):
	for sent in nltk.sent_tokenize(text):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
			if hasattr(chunk, 'node'):
				print(chunk.node, ' '.join(c[0] for c in chunk.leaves()))

articles = db.articles
indicators = db.indicators
analysis = db.analysis
named_ents = db.named_entities

named_ents.drop()

count = 0

named_entities = []

def getNodes(parent, url):
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == 'NE':
             	leaves = node.leaves()
             	ne = []
             	for leaf in leaves:
             		#print(leaf[0])
             		ne += [leaf[0]]
             	ne_url = [url] + [ne]
             	#print(ne_url)
             	
             	global named_entities
                named_entities += [ne_url]

            getNodes(node, url)


for article in articles.find():
	text = article['article_text']
	url = article['url']
	id = article['_id']
	
	words = nltk.word_tokenize(text)
	tagged = nltk.pos_tag(words)
	chunked = nltk.ne_chunk(tagged, binary=True)

	#print(chunked.height())
	getNodes(chunked, url)
	
	count = count + 1
	print(count)
	

print("Generated List")
print(count)



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
	
