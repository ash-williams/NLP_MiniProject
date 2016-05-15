from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()


def getLargestArticleWordCount():
    res = db.analysis.find({},{ "total_words": 1, "_id":0}).sort("total_words", -1).limit(1)
    rlist = list(res)
    rjson = rlist[0]
    return rjson['total_words']
    
def getLargestParagraphWordCount():
    res = db.analysis.find({},{ "paragraph_analysis.total_paragraph_word_count": 1, "_id":0})
    rlist = list(res)
    
    # print rlist 
    
    max_value = 0
    
    article_count = 0
    for r in rlist:
        article_count += 1
        res_list = r['paragraph_analysis']
        # print res_list
        for res in res_list:
            if res['total_paragraph_word_count'] > max_value:
                # print max_value
                max_value = res['total_paragraph_word_count']
    # print("Max: " + str(max_value))
    # print article_count
    return max_value
    
def getLargestSentenceWordCount():
    res = db.analysis.find({},{ "sentence_analysis.total_sentence_word_count": 1, "_id":0})
    rlist = list(res)
    
    # print rlist 
    
    max_value = 0
    
    article_count = 0
    for r in rlist:
        article_count += 1
        res_list = r['sentence_analysis']
        # print res_list
        for res in res_list:
            if res['total_sentence_word_count'] > max_value:
                # print max_value
                max_value = res['total_sentence_word_count']
    return max_value
    


