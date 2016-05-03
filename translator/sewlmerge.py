from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

#Search Engine Word List Merger
#Merges all word lists into one final word list


#Word lists
nn_wl = db.noun_word_list.find()
st_wl = db.stanford_word_list.find()
ne_wl = db.word_list.find()

fn_wl = db.final_word_list.find()

def insert_into_final(item):
    global count
    # global duplicate
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
        # print("Count: " + str(count))
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
        
        # duplicate += 1
        # print("Duplicates: " + str(duplicate))

def merge():
    count = 0
    db.final_word_list.drop()
    
    for item in nn_wl:
        insert_into_final(item)
    
    for item in st_wl:
        insert_into_final(item)
        
    for item in ne_wl:
        insert_into_final(item)
    
    #return final number of words
    return count
    