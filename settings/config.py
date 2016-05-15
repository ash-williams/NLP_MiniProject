import json

def test():
    print("Config file load test!")
    return True

# Get Config file
def getConfig(**kwargs):
    
    configFile = kwargs.get('configFile', None)
    
    path = "settings/config.json"
    
    if configFile:
        path = configFile
        
    
    with open(path) as config_file:
        return json.load(config_file)

