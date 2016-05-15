import string

from settings import config, db
from timex_events import timex

# Variables
config = config.getConfig()
db = db.getDB()



# Declare the collections
articles = db.articles

def extract(**kwargs):
    scope = kwargs.get('scope', None)
    
    if scope == "paragraph":
        event_ents = db.paragraph_event_entities
    elif scope == "sentence":
        event_ents = db.sentence_event_entities
    else:
        event_ents = db.event_entities
    
    count = 0
    
    event_ents.drop()
    event_entities = []
    
    #print(articles.count())
    
    for article in articles.find():
        text = article['article_text']
    	url = article['url']
    	
    	if scope == "paragraph":
            paragraphs = article['paragraphs']
            
            events = []
            
            for p in paragraphs:
                text = p['text']
                pnum = p['paragraph_number']
                
                found = timex.tag(text)
                if len(found) > 0:
                    events += [[found, pnum]]
            
        elif scope == "sentence":
            sentences = article['sentences']
            
            events = []
            
            for s in sentences:
                text = s['text']
                pnum = s['paragraph_number']
                snum = s['sentence_number']
                
                found = timex.tag(text)
                if len(found) > 0:
                    events += [[found, pnum, snum]]
                
        else:
            events = timex.tag(text)   
    	
     	print events
    	
        if len(events) > 0:
            final_ev = []
            
            if scope == "paragraph":
                for e in events:
                    elist = e[0]
                    pnum = e[1]
                    
                    for event in elist:
                        event = event.lower()
                        if event not in final_ev:
                            final_ev += [event]
                    ee_url = [url, final_ev, pnum]
                    event_entities += [ee_url]
                
            elif scope == "sentence":
                for e in events:
                    elist = e[0]
                    pnum = e[1]
                    snum = e[2]
                    
                    for event in elist:
                        event = event.lower()
                        if event not in final_ev:
                            final_ev += [event]
                    ee_url = [url, final_ev, pnum, snum]
                    event_entities += [ee_url]
                    
            else:
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
        
        if scope == "paragraph":
            pnum = ent[2]
        
        if scope == "sentence":
            pnum = ent[2]
            snum = ent[3]
        
        for word in words:
            if scope == "paragraph":
                doc = event_ents.find_one({"url": url, "paragraph_number": pnum})
            elif scope == "sentence":
                doc = event_ents.find_one({"url": url, "paragraph_number": pnum, "sentence_number": snum})
            else:
                doc = event_ents.find_one({"url": url})
            
            if doc:
                doc_words = doc['words']
                if word not in doc_words:
                    new_words = doc_words + [word]
                    
                    if scope == "paragraph":
                        event_ents.update({"url": url, "paragraph_number": pnum}, {"$set": {
                            "words": new_words
                        }})
                    elif scope == "sentence":
                        event_ents.update({"url": url, "paragraph_number": pnum, "sentence_number": snum}, {"$set": {
                            "words": new_words
                        }})
                    else:
                        event_ents.update({"url": url}, {"$set": {
                            "words": new_words
                        }})
            else:
                json = {
                    "url": url,
                    "words": [word]
                }
                
                if scope == "paragraph":
                    json.update({"paragraph_number": pnum})
                
                if scope == "sentence":
                    json.update({
                        "paragraph_number": pnum,
                        "sentence_number": snum
                    })
                
                event_ents.insert_one(json)
        
        
        # processForSearch(ent)
        # url = ent[0]
        # phrases = ent[1]
        
        search_terms = []
        
        for word in words:
            punctuation_exceptions = ['/', '-']
            for c in string.punctuation:
                if c in punctuation_exceptions:
                    word = word.replace(c, " ")
                else:
                    word = word.replace(c,"")
            
            phrase_list = word.split()
            
            for w in phrase_list:
                if w != "":
                    w = w.lower()
                    if w not in search_terms:
                        search_terms += [w]
        if scope == "paragraph":
            event_ents.update({"url": url, "paragraph_number": pnum}, {"$set": {
                "search_terms": search_terms
            }})
        elif scope == "sentence":
            event_ents.update({"url": url, "paragraph_number": pnum, "sentence_number": snum}, {"$set": {
                "search_terms": search_terms
            }})
        else:
            event_ents.update({"url": url}, {"$set": {
                "search_terms": search_terms
            }})
    #return number of articles searched    
    return count
    	