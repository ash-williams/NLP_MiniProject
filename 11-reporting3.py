import json
from pymongo import MongoClient
import numpy as np
import codecs

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient(config['db_url'])
db = client[config['db_client']]

articles = db.articles
analysis = db.analysis
indicators = db.indicators

min_word_count = config['min_word_count']

count = 0
avg_ind = []
avg_wc = []

html_str = """---
layout: page
title: Results Indicator Breakdown
permalink: /breakdown/
---
		<div class="container-fluid">
			<div class="table-responsive">
				<table class="table table-condensed table-hover" width="100%" style="border-collapse:collapse;">
					<thead>
						<tr>
							<!---<th>Date</th>
							<th>Title</th>--->
							<th>URL</th>"""

for indicator in indicators.find():
	html_str += "<th>" + indicator['name'] + "</th>"

html_str += """			</tr>
					<thead>
					<tbody>"""


for anal in analysis.find({"total_words": {"$gt": min_word_count}}).sort("percentage_wc_totalIncCount", -1):
    article_id = anal['article_id']
    article = articles.find_one({"_id":article_id})

    count = count + 1

    title = article['title']
    date = article['date']
    url = article['url']


    html_str += """
    	<tr data-toggle="collapse" data-target="#row""" + str(count) + """" class="accordion-toggle">
    		<!---<td>""" + str(date) + """</td>
    		<td>""" + str(title) + """</td>--->
    		<td><a href='""" + str(url) + """'>""" + str(url) + """</a></td>
    """

    for indicator in indicators.find():
        ind = indicator['name']
        i_percent = anal[ind]['percentage']
        i_percent_to_3 = '{0:.3f}'.format(i_percent)
        html_str += "<td>" + str(i_percent_to_3) + "%</td>"

    html_str += """</tr>"""



html_str += """

						</tbody>
				</table>
			</div>
		</div>
"""



with codecs.open("./site/breakdown.html",'w',encoding='utf8') as f:
    f.write(html_str)
