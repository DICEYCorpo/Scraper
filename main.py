
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os
import openai
from urllib.parse import urljoin
load_dotenv()


with open("prompts.txt", "r") as f:
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

grants_data = []
with open("cleaned_grants.txt", "r") as file:
    temp = file.readlines()
    for lines in temp:
        print(lines)
        sentence = lines.split()
        location = sentence[-2]
        search_url = "https://api.bing.microsoft.com/v7.0/search"
        search_term = lines

        headers = {"Ocp-Apim-Subscription-Key": os.getenv("SUBKEY")}
        params = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "count": 1}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        pages = (search_results['webPages'])
        results = pages['value']
        url = ""
        for result in results:
            url = result['url']

            try:
                # Send a GET request to the URL
                response = requests.get(url)

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all anchor tags <a> and extract the 'href' attribute
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and not href.startswith('#'):
                        grants_data.append([location, urljoin(url, href)])
            except requests.exceptions.ConnectTimeout:
                pass


print(grants_data)
