import string

from settings import config, db
from timex_events import timex

# Variables
config = config.getConfig()
db = db.getDB()



# Declare the collections
articles = db.articles
event_ents = db.event_entities

# For each event phrase, format ready for search engine
def processForSearch(ent):
    url = ent[0]
    phrases = ent[1]
    
    search_terms = []
    
    for phrase in phrases:
        punctuation_exceptions = ['/', '-']
        for c in string.punctuation:
            if c in punctuation_exceptions:
                phrase = phrase.replace(c, " ")
            else:
                phrase = phrase.replace(c,"")
        
        phrase_list = phrase.split()
        
        for word in phrase_list:
            if word != "":
                word = word.lower()
                if word not in search_terms:
                    search_terms += [word]
        
    event_ents.update({"url": url}, {"$set": {
        "search_terms": search_terms
    }})
        

def extract():
    count = 0
    event_ents.drop()
    event_entities = []
    
    #print(articles.count())
    
    for article in articles.find():
        text = article['article_text']
    	url = article['url']
    	
    	events = timex.tag(text)
    	
    	if len(events) != 0:
    	    final_ev = []
            for event in events:
                event = event.lower()
                if event not in final_ev:
                    final_ev += [event]
        	
            ee_url = [url, final_ev]
        	
            event_entities += [ee_url]
            count += 1
    
    #print event_entities
    for ent in event_entities:
        url = ent[0]
        words = ent[1]
        
        for word in words:
            doc = event_ents.find_one({"url": url})
            if doc:
                doc_words = doc['words']
                if word not in doc_words:
                    new_words = doc_words + [word]
                    
                    event_ents.update({"url": url}, {"$set": {
                        "words": new_words
                    }})
            else:
                json = {
                    "url": url,
                    "words": [word]
                }
                event_ents.insert_one(json)
        processForSearch(ent)

    #return number of articles searched    
    return count
    	