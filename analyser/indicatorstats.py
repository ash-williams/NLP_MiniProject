from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

# Declare the collections
articles = db.articles
indicators = db.indicators
analysis = db.analysis

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
    	
    	analysis.insert_one(data)
    	count = count + 1
    
    #return number of articles successfully analysed
    return count
    