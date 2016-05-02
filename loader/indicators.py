from settings import config, db

db = db.getDB()
config = config.getConfig()

def configTest():
    print(config.test())
    return True

def loadIndicators():
    # Drop current indicators collection
    indicators = db.indicators
    indicators.drop()
    
    # Add list of indicators from config file
    indicators_list = config['indicators']
    
    count = 0
    
    for indicator in indicators_list:
    	try:
    
    		json_indicator = {
    			"name": indicator
    		}
    		indicators.insert_one(json_indicator)
    		
    		count = count + 1
    	
    	except:
    		print("Error loading indicator: " + indicator)
    
    #return number of indicators loaded
    return(count)
