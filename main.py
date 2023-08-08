import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
load_dotenv()


with open("prompts","r") as f:
    prompts = f.read()


openai_api = os.getenv("OPENAIAPI")
openai.api_key = openai_api
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompts}
    ]
)

gpt_response = response['choices'][0]['message']['content']

with open("response.txt", "w") as tfile:
    tfile.write(gpt_response)
with open('response.txt', 'r') as tempfile:
    lines = tempfile.readlines()
# Remove the "- " from each line
cleaned_lines = [line.replace('- ', '') for line in lines]
# Write the modified lines back to the file
with open('cleaned_grants.txt', 'w') as cfile:
    cfile.writelines(cleaned_lines)



with open("cleaned_grants.txt", "r") as file:
    temp = file.readlines()
    for lines in temp:
        print(lines)
        search_url = "https://api.bing.microsoft.com/v7.0/search"
        search_term = lines

        headers = {"Ocp-Apim-Subscription-Key": os.getenv("SUBKEY")}
        params = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "count": 10}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        pages = (search_results['webPages'])
        results = pages['value']
        for result in results:
            print(result['url'])
            print()




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
