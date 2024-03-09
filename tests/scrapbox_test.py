import requests
import json

url = 'https://scrapbox.io/api/pages/christian-beginners//'

response = requests.get(url)

dictionary = json.loads(response.text)
print(dictionary['title'])
print(dictionary['descriptions'])
