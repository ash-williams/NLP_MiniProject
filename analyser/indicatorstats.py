from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

# Declare the collections
articles = db.articles
indicators = db.indicators
analysis = db.analysis

#Analyse the paragraphs and return a JSON object of results
def paragraphAnalysis(article):
    paragraph_list = article['paragraphs']
    data = []
    
    for paragraph in paragraph_list:
        para_num = paragraph['paragraph_number']
        para_text = paragraph['text']
        
        para_word_count = len(para_text.split(" "))
        
        total_para_ind_count = 0
        ind_data = {
            "paragraph_number": para_num
        }
        for indicator in indicators.find():
            ind_count = para_text.count(" " + indicator['name'] + " ")
            total_para_ind_count += ind_count
            para_ind_percentage = (100.0 * ind_count)/para_word_count
            para_ind_json = {
                indicator['name']: {
                    "count": ind_count, 
                    "percentage": para_ind_percentage
                }
            }
            ind_data.update(para_ind_json)
        ind_data.update({"total_paragraph_word_count": para_word_count})
        ind_data.update({"total_paragraph_indicator_count": total_para_ind_count})
        percentage = (100.0 * total_para_ind_count)/para_word_count
        ind_data.update({"percentage_wc_totalParaIncCount": percentage})
        
        data += [ind_data]
    #return list of results
    return data
    
def sentenceAnalysis(article):
    sentence_list = article['sentences']
    data = []
    
    for sentence in sentence_list:
        para_num = sentence['paragraph_number']
        sent_num = sentence['sentence_number']
        sent_text = sentence['text']
        
        sent_word_count = len(sent_text.split(" "))
        
        total_sent_ind_count = 0
        ind_data = {
            "paragraph_number": para_num,
            "sentence_number": sent_num
        }
        for indicator in indicators.find():
            ind_count = sent_text.count(" " + indicator['name'] + " ")
            total_sent_ind_count += ind_count
            sent_ind_percentage = (100.0 * ind_count)/sent_word_count
            sent_ind_json = {
                indicator['name']: {
                    "count": ind_count, 
                    "percentage": sent_ind_percentage
                }
            }
            ind_data.update(sent_ind_json)
        ind_data.update({"total_sentence_word_count": sent_word_count})
        ind_data.update({"total_sentence_indicator_count": total_sent_ind_count})
        percentage = (100.0 * total_sent_ind_count)/sent_word_count
        ind_data.update({"percentage_wc_totalSentIncCount": percentage})
        
        data += [ind_data]
    #return list of results
    return data
    


#Get the indicator stats and store in the analysis collection
def analyse():
    count = 0
    analysis.drop()
    
    for article in articles.find():
    	text = article['article_no_punctuation_and_lower']
    	url = article['url']
    	id = article['_id']
    	
    	data = {
    		"article_id": id,
    		"url": url
    	}
    	
    	words = text.split(' ')
    	word_count = len(words)
    	data.update({"total_words":word_count})
    	
    	total_indicator_count = 0
    	
    	for indicator in indicators.find():
    		ind_count = text.count(" " + indicator['name'] + " ")
    		total_indicator_count += ind_count
    		ind_percentage = (100.0 * ind_count)/word_count
    		ind_json = {indicator['name']: {"count": ind_count, "percentage": ind_percentage}}
    		data.update(ind_json)
    	
    	data.update({"total_indicator_count": total_indicator_count})
    	
    	percentage = (100.0 * total_indicator_count)/word_count
    	
    	data.update({"percentage_wc_totalIncCount": percentage})
    	
    	para_anal = paragraphAnalysis(article)
    	sent_anal = sentenceAnalysis(article)
    	
    	data.update({
    	    "paragraph_analysis": para_anal,
    	    "sentence_analysis": sent_anal
    	})
    	
    	analysis.insert_one(data)
    	count = count + 1
    
    #return number of articles successfully analysed
    return count
    