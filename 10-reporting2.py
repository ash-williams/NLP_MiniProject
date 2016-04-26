import json
import os
from pymongo import MongoClient
import numpy as np
import codecs

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
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
title: Results Overview
permalink: /overview/
---
		<div class="container-fluid">
			<div class="table-responsive">
				<table class="table table-condensed table-hover" width="100%" style="border-collapse:collapse;">
					<thead>
						<tr>
							<th>Date</th>
							<th>Title</th>
							<th>Word Count</th>
							<th>Indicators</th>
							<th>Percentage</th>
							<th>URL</th>
						</tr>
					</thead>
					<tbody>
"""

for anal in analysis.find({"total_words": {"$gt": min_word_count}}).sort("percentage_wc_totalIncCount", -1):
	article_id = anal['article_id']
	article = articles.find_one({"_id":article_id})

	count = count + 1

	title = article['title']
	date = article['date']
	url = article['url']

	word_count = anal['total_words']
	total_indicators = anal['total_indicator_count']
	percentage = anal['percentage_wc_totalIncCount']

	html_str += """
		<tr data-toggle="collapse" data-target="#row""" + str(count) + """" class="accordion-toggle">
			<td>""" + str(date) + """</td>
			<td>""" + str(title) + """</td>
			<td>""" + str(word_count) + """</td>
			<td>""" + str(total_indicators) + """</td>
			<td>""" + str(percentage) + """</td>
			<td><a href='""" + str(url) + """'>""" + str(url) + """</a></td>
		</tr>

	"""
	#print(title.encode())
	#print(date)
	#print(url)
	#print(word_count)
	#print(total_indicators)
	#print(percentage)

	avg_ind.append(total_indicators)
	avg_wc.append(word_count)


average_indicators = np.mean(avg_ind)
average_wordcount = np.mean(avg_wc)

html_str += """
			<tr>
				<td><strong>Total Records: </strong> """ + str(count) + """<td>
				<td><strong>Average Indicators: </strong> """ + str(average_indicators) + """<td>
				<td><strong>Average Word Count: </strong> """ + str(average_wordcount) + """<td>
			</tr>
						</tbody>
				</table>
			</div>
		</div>
"""

#print(count)

#print(average_indicators)
#print(average_wordcount)



with codecs.open("./site/overview.html",'w',encoding='utf8') as f:
    f.write(html_str)

#Html_file = open("./site/overview.html","w", "utf-8")
#Html_file.write(html_str)
#Html_file.close()
