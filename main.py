import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
search_url = "https://api.bing.microsoft.com/v7.0/search"
search_term = "Women entrepreneurs grants"

headers = {"Ocp-Apim-Subscription-Key": os.getenv("SUBKEY")}
params = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "count": 25}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

pages = (search_results['webPages'])
results = pages['value']
for result in results:
    print(result['url'])




# website = 'https://subslikescript.com/movie/Titanic-120338'
# result = requests.get(website)
# soup = BeautifulSoup(result.text, 'lxml')
#
# box = soup.find('article', class_='main-article')
#
# title = box.find('h1').get_text()
# transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')
# print(title)
# print(transcript)