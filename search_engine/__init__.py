from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask import flash, redirect, url_for, request, render_template
import json
import os
from pymongo import MongoClient
import nltk
import string

app = Flask(__name__)

ip = os.environ['IP']
port = int(os.environ['PORT'])



# # connect to MongoDB server
# app.config['MONGODB_HOST'] = ip
# #app.config['MONGODB_PORT'] = port
# app.config['MONGODB_DBNAME'] = 'uc-proto'
# app.config['MONGO_CONNECT'] = True
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

# mongo = PyMongo(app, config_prefix='MONGODB')
# mongo = MongoEngine(app)

# Get Config file
with open("../config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
db = client[config['db_client']]

if __name__ == '__main__':
    port = port
    host = ip
    app.run(port=port, host=host)
    
def register_blueprints(app):
    # Prevents circular imports
    from search_engine.views import search
    app.register_blueprint(search)

register_blueprints(app)

@app.route('/search', methods=['POST'])
def search():
    q = request.form['query']
    #results = db.articles.count()
    #flash(str(config['seed']))
    #flash(str(results))
    q = q.lower()
    
    punctuation_exceptions = ['/']
    for c in string.punctuation:
        #try:
        if c in punctuation_exceptions:
            q = q.replace(c, " ")
        else:
            q = q.replace(c,"")
    
    
    #sent tokenise
    #sentences = nltk.sent_tokenise(q)
    #word tokenise
    words = nltk.word_tokenize(q)
    
    #stop_words = set(nltk.stopwords.words("english"))
    #filtered_sentence = []
    filtered_sentence = words
    
    # for w in words:
    #     if w not in stop_words:
    #         filtered_sentence.append(w)
            
    for w in filtered_sentence:
        w = w.lower()
        
        punctuation_exceptions = ['/']
        for c in string.punctuation:
            #try:
            if c in punctuation_exceptions:
                w = w.replace(c, " ")
            else:
                w = w.replace(c,"")
            
    results_list = []
    
    if q == "all":
        res = db.word_list.find()
        for r in res:
                urls = r['urls']
                
                for url in urls:
                    if url not in results_list:
                        results_list += [url]
    else:
        for word in filtered_sentence:
            res = db.word_list.find_one({"word": word})
            if res:
                urls = res['urls']
                
                for url in urls:
                    if url not in results_list:
                        results_list += [url]
    
    # get article for each item
    article_list = []
    for url in results_list:
        article = db.articles.find_one({"url": url})
        analysis = db.analysis.find_one({"url": url})
        
        #article = article.update(analysis)
        
        article_list += [[article, analysis]]
    
    # return list
    article_list = sorted(article_list,key=lambda article_item: article_item[1]['percentage_wc_totalIncCount'], reverse=True)
        
    if len(article_list) == 0: 
        flash("No results found.")
        
    # flash(q)
    #flash(article_list[0])
    #return redirect(url_for('search', articles=article_list))
    return render_template('search.html', articles=article_list, query=q, article_count=len(article_list))


