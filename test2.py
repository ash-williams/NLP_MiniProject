# import nltk
from timex_events import timex

from settings import config
from settings import db

config = config.getConfig()
db = db.getDB()

articles = db.articles.find()
articles = articles[:100]
named_entities = []

# def getNodes(parent, url):
#     for node in parent:
#         if type(node) is nltk.Tree:
#             if node.label() == 'DATE':
#              	leaves = node.leaves()
#              	ne = []
#              	for leaf in leaves:
#              		#print(leaf[0])
#              		ne += [leaf[0]]
#              	ne_url = [url] + [ne]
#              	#print(ne_url)
             	
#              	global named_entities
#                 named_entities += [ne_url]

#             getNodes(node, url)

# print("hello")
# for article in articles:
#     text = article['article_text']
    
#     text = "Hello world, today is the 4th september 2008."
    
#     tagged = timex.tag(text)
#     print(tagged)
    
    # url = article['url']
    # print(url)
    # # words = nltk.word_tokenize(text)
    # # tagged = nltk.pos_tag(words)
    # chunked = nltk.ne_chunk(tagged)
    
    # print(chunked)
    
    # getNodes(chunked, url)
    

    # for item in named_entities:
    #     url = item[0]
    #     words = item[1]
        
    #     print("URL: " + url + "/nWords: " + str(words))



print(timex.tag("in september 2004, 8 children eat beans", returnFormat="markup"))
print(timex.tag("tomorrow is 04/04/82"))
print(timex.tag("nineteen eighty four"))
print(timex.tag("two thousand and four"))
print(timex.tag("two years later"))
print(timex.tag("two thousand and twenty four"))
print(timex.tag("during the winter, canterbury gets pretty cold. next week is 4.4.1982"))
print(timex.tag("Since the earthquakes, a lot of residents dont enjoy the city center. next tuesday is 4-4-1982"))
print(timex.tag("next week is 1982/4/4"))
print(timex.tag("in 1982, the date is 4-4-1982 and we had 2004 customers"))
print(timex.tag("in September 1985. In September, 1985. blah in September. 1985 customers.."))#, returnFormat="markup"))
