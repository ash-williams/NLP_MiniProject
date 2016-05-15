import time

from ranker import ranker as r
from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

# r.getRankingScore("http://www.joelonsoftware.com/news/fog0000000226.html")
# r.getRankingScore("http://www.joelonsoftware.com/articles/fog0000000069.html")
# r.getRankingScore("http://www.joelonsoftware.com/items/2006/09/01.html")
# r.getRankingScore("http://www.joelonsoftware.com/uibook/fog0000000249.html")

# db.ranked_results.drop()

# t0 = time.time()
# for article in db.articles.find():
#     r.insertRankedPage(article['url'])
# elapsed_time= time.time() - t0

# print("Complete in: " + str(elapsed_time) + "secs")

db.paragraph_ranked_results.drop()

t0 = time.time()
for article in db.articles.find(no_cursor_timeout=True):
    for paragraph in article['paragraphs']:
        r.insertRankedPage(article['url'], paraNo=paragraph['paragraph_number'])
elapsed_time = time.time() - t0

print("Complete in: " + str(elapsed_time) + "secs")
#Complete in: 3716.60676098secs