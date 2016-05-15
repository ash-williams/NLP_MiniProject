from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

#Search Engine Word List Merger
#Merges all word lists into one final word list

fn_wl = db.final_word_list.find()

count = 0

def insert_into_final(item, final_wl):
    global count
    # global duplicate
    word = item['word']
    urls = item['urls']
    
    print item
    
    # print(urls)
    
    exists = final_wl.find_one({"word": word})
    if not exists:
        json = {
            "word": word,
            "urls": urls
        }
        final_wl.insert_one(json)
        count += 1
        # print("Count: " + str(count))
    else:
        existing_urls = exists['urls']
        
        for url in urls:
            if url in existing_urls:
                print("Nothing to do")
            else:
                new_urls = existing_urls + [url]
                
                final_wl.update({"word": word}, {"$set": {
                    "urls": new_urls,
                }})
        
        # duplicate += 1
        # print("Duplicates: " + str(duplicate))

def merge(**kwargs):
    scope = kwargs.get('scope', None)
    
    
    if scope == "paragraph":
        # print("para")
        nn_wl = db.paragraph_noun_word_list.find()
        st_wl = db.paragraph_stanford_word_list.find()
        ne_wl = db.paragraph_word_list.find()
    elif scope == "sentence":
        # print("sent")
        nn_wl = db.sentence_noun_word_list.find()
        st_wl = db.sentence_stanford_word_list.find()
        ne_wl = db.sentence_word_list.find()
    else:
        # print("arti")
        nn_wl = db.noun_word_list.find()
        st_wl = db.stanford_word_list.find()
        ne_wl = db.word_list.find()
        
    if scope == "paragraph":
        final_wl = db.paragraph_final_word_list
    elif scope == "sentence":
        final_wl = db.sentence_final_word_list
    else:
        final_wl = db.final_word_list
    
    
    final_wl.drop()
    
    for item in nn_wl:
        # print item
        insert_into_final(item, final_wl)
    
    for item in st_wl:
        # print item
        insert_into_final(item, final_wl)
        
    for item in ne_wl:
        # print item
        insert_into_final(item, final_wl)
    
    #return final number of words
    return count
    