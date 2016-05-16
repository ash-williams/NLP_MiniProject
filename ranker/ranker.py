from analyser import genericstats as stats
from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

#Takes in URL and returns a ranking score out of
#100 for that page
#for paragraph and sentences, accepts pnum and snum
def getRankingScore(url, **kwargs):
    pnum = kwargs.get('paraNo', None)
    snum = kwargs.get('sentNo', None)
    
    # print pnum, snum
    
    if pnum != None:
        if snum != None:
            e_type = "sentence"
            snum = int(snum)
            pnum = int(pnum)
        else:
            e_type = "paragraph"
            pnum = int(pnum)
    else:
        e_type = "article"
    
    # print e_type
    
    if e_type == "paragraph":
        max_wc = stats.getLargestParagraphWordCount()
        
        ne_words = []
        ee_words = []
        
        analysis = db.analysis.find_one({"url":url})
        ne = db.paragraph_named_entities.find_one({"url":url, "paragraph_number": pnum})
        ee = db.paragraph_event_entities.find_one({"url":url, "paragraph_number": pnum})
        
        if ne:
            ne_words = ne['words']
        
        if ee:
            ee_words = ee['words']
        
        para_anal = analysis['paragraph_analysis']
        
        for para in para_anal:
            # print para
            if para['paragraph_number'] == pnum:
                in_cnt = para['total_paragraph_indicator_count']
                wc_cnt = para['total_paragraph_word_count']
                # print in_cnt, wc_cnt
            
        ne_cnt = len(ne_words)
        ee_cnt = len(ee_words)
        
    elif e_type == "sentence":
        max_wc = stats.getLargestSentenceWordCount()
        
        ne_words = []
        ee_words = []
        
        analysis = db.analysis.find_one({"url":url})
        ne = db.paragraph_named_entities.find_one({"url":url, "paragraph_number": pnum, "sentence_number": snum})
        ee = db.paragraph_event_entities.find_one({"url":url, "paragraph_number": pnum, "sentence_number": snum})
        
        if ne:
            ne_words = ne['words']
        
        if ee:
            ee_words = ee['words']
        
        sent_anal = analysis['sentence_analysis']
        
        for sent in sent_anal:
            # print para
            if sent['paragraph_number'] == pnum and sent['sentence_number'] == snum:
                in_cnt = sent['total_sentence_indicator_count']
                wc_cnt = sent['total_sentence_word_count']
                # print in_cnt, wc_cnt
            
        ne_cnt = len(ne_words)
        ee_cnt = len(ee_words)
        
    else:
        max_wc = stats.getLargestArticleWordCount()
        
        ne_words = []
        ee_words = []
        
        analysis = db.analysis.find_one({"url":url})
        ne = db.named_entities.find_one({"url":url})
        ee = db.event_entities.find_one({"url":url})
        
        if ne:
            ne_words = ne['words']
        
        if ee:
            ee_words = ee['words']
        
        in_cnt = analysis['total_indicator_count']
        ne_cnt = len(ne_words)
        ee_cnt = len(ee_words)
        wc_cnt = analysis['total_words']
    
    # print in_cnt, ne_cnt, ee_cnt, wc_cnt, max_wc
    
    score = 0
    
    score += ((100.0 * in_cnt)/wc_cnt)
    score += ((100.0 * ne_cnt)/wc_cnt)
    score += ((100.0 * ee_cnt)/wc_cnt)
    
    
    score += ((100.0 * wc_cnt)/max_wc)
    
    if e_type == "article":
        min_wc = config['min_word_count']
    
    if e_type == "sentence":
        min_wc = config['sentence_min_word_count']
        
    if e_type == "paragraph":
        min_wc = config['paragraph_min_word_count']
        
    if wc_cnt > min_wc:
        score += 100
    
    # print score
    
    return score
    
#Takes in URL, works out ranking score and returns
#true if successfully inserted
#for paragraph and sentences, accepts pnum and snum
def insertRankedPage(url, **kwargs):
    pnum = kwargs.get('paraNo', None)
    snum = kwargs.get('sentNo', None)
    
    if pnum != None:
        if snum != None:
            e_type = "sentence"
            snum = int(snum)
        else:
            e_type = "paragraph"
            pnum = int(pnum)
    else:
        e_type = "article"
    
    # print e_type
    
    if e_type == "paragraph":
        ranked_results = db.paragraph_ranked_results
        
        doc = ranked_results.find_one({"url": url, "paragraph_number": pnum })
        if not doc:
            score = getRankingScore(url, paraNo=pnum)
            
            ranked_results.insert_one({
                "url": url,
                "paragraph_number": pnum,
                "score": score
            })
    elif e_type == "sentence":
        ranked_results = db.sentence_ranked_results
        
        doc = ranked_results.find_one({"url": url, "paragraph_number": pnum, "sentence_number": snum})
        if not doc:
            score = getRankingScore(url, paraNo=pnum, sentNo=snum)
            
            ranked_results.insert_one({
                "url": url,
                "paragraph_number": pnum,
                "sentence_number": snum,
                "score": score
            })
    else:
        ranked_results = db.ranked_results
        
        doc = ranked_results.find_one({"url": url})
        if not doc:
            score = getRankingScore(url)
            
            # print "insert new"
            try:
                ranked_results.insert_one({
                    "url": url,
                    "score": score
                })
            except:
                print("Unexpected error:", sys.exc_info()[0])
    return True

