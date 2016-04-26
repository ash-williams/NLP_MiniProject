from search_engine import mongo

class Word(mongo.Document):
    word = mongo.StringField()
    urls = mongo.ListField(mongo.StringField())