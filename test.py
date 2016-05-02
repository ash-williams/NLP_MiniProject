# import json
# import os
# from pymongo import MongoClient
# import nltk
# from nltk.sem import relextract
# import re
# from settings import config
from settings import db
# import sys
# from loader import indicators

# # sys.path.append("/home/ubuntu/workspace/")
# # print(sys.path)

# x = indicators.configTest()

# config = config.getConfig()
db = db.getDB()


#for translator
collection = "final_word_list"
print(db[collection].count())


#cleaner
from bs4 import BeautifulSoup
body = '<body><div class="hello">Sup</div></body>'
dclass = "hello"
soup = BeautifulSoup(body, "html5lib")
test = soup.find('div', {"class": dclass}).getText()
print(test)


# print(config['indicators'])

# res = db.final_word_list.find_one({"word": "java"})
# print(res)
# s = "Hello.World.NET"



# text = re.sub(r'\.([a-zA-Z])([a-z ])', r'. \1\2', s)

# print(text)


# # Get Config file
# with open("config.json") as config_file:
#     config = json.load(config_file)

# # Connect to mongo
# client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
# db = client[config['db_client']]

# named_ents = db.named_entities
# word_list = db.word_list

# stanford_named_ents = db.stanford_named_entities
# stanford_word_list = db.stanford_word_list

# noun_named_ents = db.noun_named_entities
# noun_word_list = db.noun_word_list

# ne_words = word_list.find()
# st_words = stanford_word_list.find()
# nn_words = noun_word_list.find()

# itemCnt = 0
# stItemCnt = 0
# nnItemCnt = 0
# missingCnt = 0
# stMissingCnt = 0
# nnMissingCnt = 0

# st_wl = []
# for item in st_words:
#     word = item['word']
#     if word not in st_wl:
#         st_wl += [word]

# ne_wl = []
# for item in ne_words:
#     word = item['word']
#     if word not in ne_wl:
#         ne_wl += [word]
        
# nn_wl = []
# for item in nn_words:
#     word = item['word']
#     if word not in nn_wl:
#         nn_wl += [word]
        
# print(len(st_wl))
# print(len(ne_wl))
# print(len(nn_wl))

# print("words not in stanford and noun")
# for word in ne_wl:
#     itemCnt += 1
#     if word not in st_wl and word not in nn_wl:
#         missingCnt += 1
#         #print(word)

# print(itemCnt)
# print(missingCnt)
# print("*******************************")
        
# print("words not in ne and noun")
# for word in st_wl:
#     stItemCnt += 1
#     if word not in ne_wl and word not in nn_wl:
#         stMissingCnt += 1
#         #print(word)

# print(stItemCnt)
# print(stMissingCnt)

# print("*******************************")
        
# print("words not in ne and stanford")
# for word in nn_wl:
#     nnItemCnt += 1
#     if word not in ne_wl and word not in st_wl:
#         nnMissingCnt += 1
#         #print(word)

# print(nnItemCnt)
# print(nnMissingCnt)

# print("********************************")
# res = db.word_list.find_one({"word":"frameworks"})

# urls = res['urls']

# print(len(urls))
    