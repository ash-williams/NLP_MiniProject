from pymongo import MongoClient

#Connect to mongo
client = MongoClient('mongodb://localhost/27017')
db = client['uc-proto']

indicators = db.indicators

indicators.drop()


indicators_list = [
'therefore',
'so',
'hence',
'consequently',
'because',
'for',
'since',
'when',
'then',
'next',
'who',
'we',
'they',
'do',
'doing',
'did',
'thats',
'in particular',
'but',
'know',
'not'
]


count = 0

for indicator in indicators_list:
	try:

		json_indicator = {
			"name": indicator
		}
		indicators.insert_one(json_indicator)
		
		count = count + 1
	
	except:
		print("Error")

print(count)
	
