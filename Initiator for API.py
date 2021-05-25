from IPython.display import HTML
import requests
import json
import pandas as pd
import numpy as np
import datetime

# bing news search API
'''
url = "https://bing-news-search1.p.rapidapi.com/news"
search_term = "gold price"

querystring = {"q": search_term, "mkt": "en-US", "safeSearch": "Off",
               "category": "Business", "setLang": "EN", "textFormat": "Raw"}

headers = {
    'x-rapidapi-host': "bing-news-search1.p.rapidapi.com",
    'x-rapidapi-key': "ec7cf83d7amsh28327258127105bp16fa52jsn9cf67d1e4463",
    'x-bingapis-sdk': "true"
}

response = requests.request("GET", url, headers=headers, params=querystring)
response.raise_for_status()
search_results = json.loads(json.dumps(response.json()))

descriptions = [article["description"] for article in search_results["value"]]
print(descriptions)
rows = "\n".join(["<tr><td>{0}</td></tr>".format(desc)
                  for desc in descriptions])
HTML("<table>"+rows+"</table>")
'''

'''
# Bloomberg API
# All tracked data. Can be used to get the ticker name/symbol
url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/auto-complete"

querystring = {"query": "gold"}

headers = {
    'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com",
    'x-rapidapi-key': "ec7cf83d7amsh28327258127105bp16fa52jsn9cf67d1e4463"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

# stock chart
url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/get-chart"

# m1 = 1 month period, id: company:country (ibm:us -> ibm%3Aus)
querystring = {"interval": "m1", "id": "ibm%3Aus"}

headers = {
    'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com",
    'x-rapidapi-key': "ec7cf83d7amsh28327258127105bp16fa52jsn9cf67d1e4463"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# returns data in form of ticks. For m1, each tick is 1 trading day.
print(response.text)
'''

# generic google search using search query


def extract_news():
    url = "https://google-news.p.rapidapi.com/v1/search"
    querystring = {"lang": "en", "q": "Gold"}
    headers = {
        'x-rapidapi-host': "google-news.p.rapidapi.com",
        'x-rapidapi-key': "ec7cf83d7amsh28327258127105bp16fa52jsn9cf67d1e4463"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    json_d = response.json()
    return json_d

# google topic search of topics in google.
# For example, if you search for corona in the search tab of en + US you will find COVID-19 as a topic.
# The URL looks like this: https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hsNUVnSmxiaWdBUAE?hl=en-US&gl=US&ceid=US%3Aen
# We have to copy the text after topics/ and before ?, then you can use it as an input for the topic parameter: CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hsNUVnSmxiaWdBUAE
#Gold: CAAqJAgKIh5DQkFTRUFvS0wyMHZNREkxY25NeWVoSUNaVzRvQUFQAQ


def extract_news2():
    url = "https://google-news.p.rapidapi.com/v1/topic_headlines"
    querystring = {
        "lang": "en", "topic": "CAAqJAgKIh5DQkFTRUFvS0wyMHZNREkxY25NeWVoSUNaVzRvQUFQAQ"}
    headers = {
        'x-rapidapi-host': "google-news.p.rapidapi.com",
        'x-rapidapi-key': "ec7cf83d7amsh28327258127105bp16fa52jsn9cf67d1e4463"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    json_d = response.json()
    return json_d


json_d = extract_news2()
print(json_d)
