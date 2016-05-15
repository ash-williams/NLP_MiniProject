# import urllib3
# import sys
# from bs4 import BeautifulSoup
# import nltk

# url = "http://www.joelonsoftware.com/articles/fog0000000069.html"

# http_pool = urllib3.connection_from_url(url)
# r = http_pool.urlopen('GET',url)
# html = r.data.decode('utf-8')

# soup = BeautifulSoup(html, "html5lib")


# from_pos = soup.find('div', {"class": "date"})
# to_pos = soup.find('br', {"clear":"all"})

# text = ""
# paragraphs = []
# sentences = []

# para_count = 0

# for tag in from_pos.next_siblings:
# 	if tag == to_pos:
# 		break
# 	else:
# 		try:
# 			p = tag.text

# 			text += p + " "
# 			paragraphs += [{
#         			    "paragraph_number": para_count,
#         			    "text": p
#     			    }]
# 			para_count = para_count + 1
# 		except: 
# 			print("Unexpected error:", sys.exc_info())
			
# for p in paragraphs:
# 	pcount = p['paragraph_number']
# 	text = p['text']
# 	s = nltk.sent_tokenize(text)
# 	sent_count = 0
# 	for sent in s:
# 		sentences += [{
#     		        "sentence_number": sent_count, 
#     		        "paragraph_number": pcount,
#     		        "text": sent
#     		    }]
# 		sent_count += 1

# print text

# x = text.split()
# print len(x)

# print paragraphs
# print len(paragraphs)

# print sentences
# print len(sentences)


from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

# res = db.analysis.find_one({"url" : "http://www.joelonsoftware.com/articles/fog0000000069.html"})

# print len(res['paragraph_analysis'])
# print "************************************"
# print len(res['sentence_analysis'])

# print res['paragraph_analysis']

from analyser import genericstats

# x = genericstats.getLargestArticleWordCount()
# y = genericstats.getLargestParagraphWordCount()
z = genericstats.getLargestSentenceWordCount()

# print x
# print y
print z