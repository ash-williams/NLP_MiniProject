import json

def test():
    print("Config file load test!")
    return True

# Get Config file
def getConfig():
    with open("settings/config.json") as config_file:
        return json.load(config_file)

