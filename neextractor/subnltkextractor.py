import nltk

from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

named_entities = []

# Declare the collections
articles = db.articles
indicators = db.indicators
analysis = db.analysis


def getNodes(parent, url, **kwargs):
    pnum = kwargs.get('paraNo', None)
    snum = kwargs.get('sentNo', None)
    
    # print("Pnum:" + str(pnum))
    # print("Snum:" + str(snum))
    
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == 'NE':
             	leaves = node.leaves()
             	ne = []
             	for leaf in leaves:
             		#print(leaf[0])
             		ne += [leaf[0]]
             	
             	ne_url = [url] + [ne]
                #  	print("one")
             	if pnum != None:
                    if snum != None:
                        # print("two")
                        ne_url += [pnum, snum]
                    else:
                        # print("tree")
                        ne_url += [pnum]

             	
             	#print(ne_url)
             	
             	global named_entities
                named_entities += [ne_url]

            getNodes(node, url)

def extract(**kwargs):
    #Can be text/paragraph/sentence
    extract_type = kwargs.get('extract_type', None)
    
    if extract_type == "paragraph":
        named_ents = db.paragraph_named_entities
    elif extract_type == "sentence":
        named_ents = db.sentence_named_entities
    else:
        named_ents = db.named_entities
        
    count = 0
    named_ents.drop()
    
    articles_list = articles.find(no_cursor_timeout=True)
    # articles_list = articles_list[:1]
    
    for article in articles_list:
    	text = article['article_text']
    	url = article['url']
    	
    	if extract_type == "paragraph":
    	    paragraphs = article['paragraphs']
    	    
    	    for p in paragraphs:
    	        text = p['text']
    	        num = p['paragraph_number']
    	        words = nltk.word_tokenize(text)
            	tagged = nltk.pos_tag(words)
            	chunked = nltk.ne_chunk(tagged, binary=True)
            
            	getNodes(chunked, url, paraNo=num)
        elif extract_type == "sentence":
            sentences = article['sentences']
            
            for s in sentences:
                text = s['text']
                pnum = s['paragraph_number']
                snum = s['sentence_number']
                words = nltk.word_tokenize(text)
            	tagged = nltk.pos_tag(words)
            	chunked = nltk.ne_chunk(tagged, binary=True)
            
            	getNodes(chunked, url, paraNo=pnum, sentNo=snum)
        else:
        	words = nltk.word_tokenize(text)
        	tagged = nltk.pos_tag(words)
        	chunked = nltk.ne_chunk(tagged, binary=True)
        
        	getNodes(chunked, url)
    	print count
    	count += 1
    
    print named_entities
    
    insert_count = 0	
    for item in named_entities:
        print item
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
                print("existing record")
                doc_words = doc['words']
                if word not in doc_words:
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
                print("New record")
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
                print(json)
                named_ents.insert_one(json)
        print insert_count
        insert_count += 1
    
    #return number of articles extracted
    return count
    
	