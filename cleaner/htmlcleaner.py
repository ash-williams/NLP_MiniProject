import sys
import urllib3
from bs4 import BeautifulSoup
import string
import nltk

from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

# Declare the collections
pages = db.pages
articles = db.articles

#Get meta information - specific to Joel on Software
#Returns JSON object of meta data
def getMeta(soup):
    # Meta indicators - specific to Joel on software
	title = soup.find('h2').getText()
	author = soup.find('div', {"class": "author"}).getText()
	date = soup.find('div', {"class": "date"}).getText()
	
	#trim author
	if author.startswith('by '):
		author = author[3:]
	
	#extract date
	split_date = date.split(' ')
	dow = split_date[0][:-1]
	month = split_date[1]
	day = split_date[2][:-1]
	year = split_date[3]
	
	json_article = {
		"title": title,
		"author": author,
		"date": date,
		"dow": dow,
		"day": day,
		"month": month,
		"year": year
	}
	return json_article
	
#Extracts the articles text - specific to Joel on Software
#Returns a JSON object with the article_text
def getArticleText(soup):
    from_pos = soup.find('div', {"class": "date"})
    to_pos = soup.find('br', {"clear":"all"})
	
    text = ""
    paragraphs = []
    sentences = []
    
    para_count = 0
	
    for tag in from_pos.next_siblings:
        if tag == to_pos:
            break
        else:
            try:
                p = tag.text

                text += p + " "
                paragraphs += [{
                    "paragraph_number": para_count,
                    "text": p
                }]
                para_count = para_count + 1
            except: 
                print("Unexpected error:", sys.exc_info()[0])
	
	error_cnt = 0			
    for p in paragraphs:
        try: 
            pcount = p['paragraph_number']
            ptext = p['text']
            s = nltk.sent_tokenize(ptext)
            sent_count = 0
            for sent in s:
                sentences += [{
                    "sentence_number": sent_count, 
                    "paragraph_number": pcount,
                    "text": sent
                }]
                sent_count += 1
        except:
            error_cnt += 1
            print("Unexpected error:", sys.exc_info()[0])
    
    print error_cnt
	
    text_no_punctuation = text
    punctuation_exceptions = ['/']
    
    for c in string.punctuation:
        if c in punctuation_exceptions:
            text_no_punctuation = text_no_punctuation.replace(c, " ")
        else:
            text_no_punctuation = text_no_punctuation.replace(c,"")
	
	text_no_punctuation_lower = text_no_punctuation.lower()
	
    json = {
        "article_text": text,
        "article_no_punctuation": text_no_punctuation,
        "article_no_punctuation_and_lower": text_no_punctuation_lower,
        "paragraphs": paragraphs,
        "sentences": sentences
    }
    return json
	
	
	
#Clean HTML into article collection
def clean():
    articles.drop()
    count = 0
    
    for page in pages.find():
    	body = page['body']
    	id = page['_id']
    	url = page['url']
    	
    	try:
            soup = BeautifulSoup(body, "html5lib")
	        
            json = {
                "url": url,
                "page_id": id
            }
	    
            json.update(getMeta(soup))
            json.update(getArticleText(soup))
            
            articles.insert_one(json)
            count = count + 1
    	except:
    		print("Unexpected error:", sys.exc_info()[0])
    #Return count of number of successful cleans
    return count