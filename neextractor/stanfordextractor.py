from nltk.tag import StanfordNERTagger
import string, sys

from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

st = StanfordNERTagger("classifiers/english.conll.4class.distsim.crf.ser.gz", "classifiers/stanford-ner.jar")#"/usr/share/stanford-ner/classifiers/all.3class.distsim.crf.ser.gz", "/usr/share/stanford-ner/stanford-ner.jar")

# Declare the collections
articles = db.articles
indicators = db.indicators
analysis = db.analysis
stanford_named_ents = db.stanford_named_entities

def extract():
    count = 0
    stanford_named_ents.drop()
    
    for article in articles.find(no_cursor_timeout=True):
        try:
            text = article['article_text']
            url = article['url']
        	
            if not (stanford_named_ents.find_one({"url": url})):
                tagged = st.tag(text.split())
                words = []
                
                for word in tagged:
                    #print(word[1])
                    if word[1] != 'O':
                        if word[0] not in words:
                            word = word[0]
                            punctuation_exceptions = ['/', '-']
                            for c in string.punctuation:
                                if c in punctuation_exceptions:
                                    word = word.replace(c, " ")
                                else:
                                    word = word.replace(c,"")
                            
                            split = word.split(" ")
                            for word in split:
                                if word != '':
                                    words += [word]
                
                for word in words:
            		doc = stanford_named_ents.find_one({"url": url})
            		if doc:
            			doc_words = doc['words']
            			if word not in doc_words:
            				new_words = doc_words + [word]
            				
            				stanford_named_ents.update({"url": url }, {"$set": {
            				 	"words": new_words,
            				}})	
            		
            		else:
            			json = {
            						"url": url,
            						"words": [word]
            					}
            			stanford_named_ents.insert_one(json)
                
                
            count = count + 1
        except:
            print("Unexpected error:", sys.exc_info()[0])
    #return number of articles extracted
    return count
