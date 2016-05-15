from nltk.tag import StanfordNERTagger
import string, sys

from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

named_entities = []

st = StanfordNERTagger("classifiers/english.conll.4class.distsim.crf.ser.gz", "classifiers/stanford-ner.jar")#"/usr/share/stanford-ner/classifiers/all.3class.distsim.crf.ser.gz", "/usr/share/stanford-ner/stanford-ner.jar")

# Declare the collections
articles = db.articles
indicators = db.indicators
analysis = db.analysis

def extract(**kwargs):
    #Can be text/paragraph/sentence
    extract_type = kwargs.get('extract_type', None)
    
    global named_entities
    
    if extract_type == "paragraph":
        stanford_named_ents = db.paragraph_stanford_named_entities
    elif extract_type == "sentence":
        stanford_named_ents = db.sentence_stanford_named_entities
    else:
        stanford_named_ents = db.stanford_named_entities
        
    count = 0
    stanford_named_ents.drop()
    
    for article in articles.find(no_cursor_timeout=True):
        try:
            text = article['article_text']
            url = article['url']
            
            if extract_type == "paragraph":
                paragraphs = article['paragraphs']
                
                for p in paragraphs:
                    text = p['text']
                    pnum = p['paragraph_number']
                    
                    
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
                    ne_url = [url] + [words] + [pnum]
                    named_entities += [ne_url]  
                    
            
            elif extract_type == "sentence":
                sentences = article['sentences']
                
                for s in sentences:
                    text = s['text']
                    pnum = s['paragraph_number']
                    snum = s['sentence_number']
                    
                    
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
                    ne_url = [url] + [words] + [pnum, snum]
                    named_entities += [ne_url]
                
            else:
                
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
                ne_url = [url] + [words]
                named_entities += [ne_url] 
            print count
            count += 1
            #print named_entities
        except:
            print("Unexpected error:", sys.exc_info()[0])
     
    insert_count = 0       
    for item in named_entities:
        url = item[0]
        words = item[1]
        
        if len(item) == 3:
    	    pnum = item[2]
    	 
    	if len(item) == 4:
    	    pnum = item[2]
    	    snum = item[3]
        
        
        for word in words:
            if extract_type == "paragraph":
                doc = stanford_named_ents.find_one({"url": url, "paragraph_number": pnum})
            elif extract_type == "sentence":
                doc = stanford_named_ents.find_one({"url": url, "paragraph_number": pnum, "sentence_number": snum})
            else:
            	doc = stanford_named_ents.find_one({"url": url})
            print doc
            if doc:
                doc_words = doc['words']
                if word not in doc_words:
                    print("new word to existing record")
                    new_words = doc_words + [word]
                    
                    if extract_type == "paragraph":
                        stanford_named_ents.update({"url": url, "paragraph_number": pnum }, {"$set": {
                            "words": new_words,
                        }})	
                    elif extract_type == "sentence":
                        stanford_named_ents.update({"url": url, "paragraph_number": pnum, "sentence_number": snum}, {"$set": {
                            "words": new_words,
                        }})	
                    else:
                        stanford_named_ents.update({"url": url }, {"$set": {
                            "words": new_words,
                        }})	
            else:
                print("new record")
                json = {
                    "url": url,
                    "words": [word]
                }
        				
                if len(item) == 3:
                    json.update({"paragraph_number": pnum})
                
                if len(item) == 4:
                    json.update({
                        "paragraph_number": pnum,
                        "sentence_number": snum
                    })
                stanford_named_ents.insert_one(json)
                
        print insert_count        
        insert_count += 1
        
    #return number of articles extracted
    return count
