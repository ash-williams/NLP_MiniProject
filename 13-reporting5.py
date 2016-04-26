import json
from pymongo import MongoClient
import numpy as np
import codecs
import os

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
db = client[config['db_client']]

word_list = db.word_list
articles = db.articles

### Search Engine
def query(search_string):
    

