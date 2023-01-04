import requests
import json

# Open config file
config_file = open('config.json')
config = json.load(config_file)

query = {'key': config['api_key'], 'q': 'Lille'}
response = requests.get("https://api.weatherapi.com/v1/current.json", params=query)

json_response = response.json()
print(json_response)