import string, re, nltk, unicodedata

from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

named_entities = []

# Declare the collections
articles = db.articles
indicators = db.indicators
analysis = db.analysis

#takes in tagged string, returns list of words
def getWords(tagged):
    words = []
    
    for item in tagged:
        if item[1] in config['noun_extraction_list']:
            word = item[0]
            
            word = word.lower()
            word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore')
            
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
    return words       
    
    

def extract(**kwargs):
    #Can be text/paragraph/sentence
    extract_type = kwargs.get('extract_type', None)
    
    global named_entities
    
    if extract_type == "paragraph":
        named_ents = db.paragraph_noun_named_entities
    elif extract_type == "sentence":
        named_ents = db.sentence_noun_named_entities
    else:
        named_ents = db.noun_named_entities
    
    
    count = 0
    named_ents.drop()
    
    for article in articles.find(no_cursor_timeout=True):
        text = article['article_text']
        url = article['url']
        
        if extract_type == "paragraph":
            paragraphs = article['paragraphs']
            
            for p in paragraphs:
                text = p['text']
                pnum = p['paragraph_number']
                
                text = re.sub(r'\.([a-zA-Z"])([a-z ])', r'. \1\2', text)
                
                words = nltk.word_tokenize(text)
                tagged = nltk.pos_tag(words)
                
                words = getWords(tagged)
                
                ne_url = [url] + [words] + [pnum]
                named_entities += [ne_url]
                
        elif extract_type == "sentence":
            sentences = article['sentences']
            
            for s in sentences:
                text = s['text']
                pnum = s['paragraph_number']
                snum = s['sentence_number']
                
                text = re.sub(r'\.([a-zA-Z"])([a-z ])', r'. \1\2', text)
                
                words = nltk.word_tokenize(text)
                tagged = nltk.pos_tag(words)
                
                words = getWords(tagged)
                
                ne_url = [url] + [words] + [pnum, snum]
                named_entities += [ne_url]
        else:
            text = re.sub(r'\.([a-zA-Z"])([a-z ])', r'. \1\2', text)
            
            words = nltk.word_tokenize(text)
            tagged = nltk.pos_tag(words)
            
            words = getWords(tagged)
                   
            ne_url = [url] + [words]
            named_entities += [ne_url]
        print count
        count += 1
        
    print named_entities
    
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
                doc = named_ents.find_one({"url": url, "paragraph_number": pnum})
            elif extract_type == "sentence":
                doc = named_ents.find_one({"url": url, "paragraph_number": pnum, "sentence_number": snum})
            else:
                doc = named_ents.find_one({"url": url})
            print doc
            if doc:
                doc_words = doc['words']
                if word in doc_words:
                    print("URL and word already exists")
                else:
                    print("new word to existing record")
                    new_words = doc_words + [word]
                    if extract_type == "paragraph":
                        named_ents.update({"url": url, "paragraph_number": pnum}, {"$set": {
                            "words": new_words,
                        }})	
                    elif extract_type == "sentence":
                        named_ents.update({"url": url, "paragraph_number": pnum, "sentence_number": snum}, {"$set": {
                            "words": new_words,
                        }})	
                    else:
                        named_ents.update({"url": url}, {"$set": {
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
                named_ents.insert_one(json)
        print insert_count
        insert_count += 1
    #return number of articles extracted
    return count
    	
