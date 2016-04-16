<<<<<<< HEAD
import json
from pymongo import MongoClient
import numpy as np

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

html_str = """
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>Indicator Analysis Results</title>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
		
		<style>
			.hiddenRow {
				padding: 0 !important;
			}
		</style>
	
	</head>
	<body>
		<div class="container-fluid">
			<h1>Results of Indicator Analysis</h1>
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
							<th></th>
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
			<td>""" + str(url) + """</td>
		</tr>
		<tr >
            <td colspan="6" class="hiddenRow">
				<div class="accordian-body collapse" id="row""" + str(count) + """">
					<table class="table table-condensed">
						<thead>
						<tr>"""
						
	for indicator in indicators.find():
		html_str += "<th>" + indicator['name'] + "</th>"
								
	html_str += """			</tr>
						<thead>
						<tbody>"""
						
	for indicator in indicators.find():
		ind = indicator['name']
		i_percent = anal[ind]['percentage']
		i_percent_to_3 = '{0:.3f}'.format(i_percent)
		html_str += "<td>" + str(i_percent_to_3) + "%</td>"
							
	html_str += """		<tbody>
					</table>
				</div>
			</td>
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
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
	</body>
</html>
"""
	
#print(count)

#print(average_indicators)
#print(average_wordcount)

Html_file = open("results.html","w")
Html_file.write(html_str)
Html_file.close()
	
	
	
=======
import json
from pymongo import MongoClient
import numpy as np

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

html_str = """
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>Indicator Analysis Results</title>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
		
		<style>
			.hiddenRow {
				padding: 0 !important;
			}
		</style>
	
	</head>
	<body>
		<div class="container-fluid">
			<h1>Results of Indicator Analysis</h1>
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
							<th></th>
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
			<td>""" + str(url) + """</td>
		</tr>
		<tr >
            <td colspan="6" class="hiddenRow">
				<div class="accordian-body collapse" id="row""" + str(count) + """">
					<table class="table table-condensed">
						<thead>
						<tr>"""
						
	for indicator in indicators.find():
		html_str += "<th>" + indicator['name'] + "</th>"
								
	html_str += """			</tr>
						<thead>
						<tbody>"""
						
	for indicator in indicators.find():
		ind = indicator['name']
		i_percent = anal[ind]['percentage']
		i_percent_to_3 = '{0:.3f}'.format(i_percent)
		html_str += "<td>" + str(i_percent_to_3) + "%</td>"
							
	html_str += """		<tbody>
					</table>
				</div>
			</td>
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
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
	</body>
</html>
"""
	
#print(count)

#print(average_indicators)
#print(average_wordcount)

Html_file = open("results.html","w")
Html_file.write(html_str)
Html_file.close()
	
	
	
>>>>>>> d60802d8e614c209359ffbcff608940a2dce4ea3
