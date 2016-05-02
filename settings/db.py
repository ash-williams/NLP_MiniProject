import os #for cloud nine only

from pymongo import MongoClient
from . import config

config = config.getConfig()

# Connect to mongo, returns db
def getDB():
    client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
    return client[config['db_client']]


