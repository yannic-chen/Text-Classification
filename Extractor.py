import requests
import json
from newspaper import Article
from newspaper import Config
import pathlib
import os
import re
import time
import numpy as np
import datetime

# Datetime check for comparing newsarticle publish date
today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)

# user_agent specification. Dont know if it is necessary. Mixed results
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

# extract all URLs from Google topics


def extract_news2():
    url = "https://google-news.p.rapidapi.com/v1/topic_headlines"
    querystring = {
        "lang": "en", "topic": "CAAqJAgKIh5DQkFTRUFvS0wyMHZNREkxY25NeWVoSUNaVzRvQUFQAQ"}  # the long topic alphanumerical code stands for "gold"
    headers = {
        'x-rapidapi-host': "google-news.p.rapidapi.com",
        'x-rapidapi-key': "ec7cf83d7amsh28327258127105bp16fa52jsn9cf67d1e4463"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    json_d = response.json()
    return json_d


json_d = extract_news2()
temp_number = len(json_d["articles"])
print("found articles:", temp_number)
with open("log.txt", "a") as f:
    f.write(str(datetime.datetime.now()) + "\n")
    f.write(f"found articles: {temp_number} \n")

# create a dictionary will all the titles and links. Append all found articles if they have specific words in their title.
gold = {"title": [], "link": []}
for i in json_d["articles"]:
    # dont need to look for words in title. The NLP keywords filter does a good enough job
    '''
    if "gold" or "Gold" or "GOLD" or "XAU" in i["title"]:
        gold["title"].append(i["title"])
        gold["link"].append(i["link"])
    '''
    gold["title"].append(i["title"])
    gold["link"].append(i["link"])

#print("articles with gold:", len(gold["link"]))

# load the keywords data into a dictionary. This is done to further reduce articles based on their text content.
keywords = np.load('keywords.npy', allow_pickle='TRUE').item()
# this keyword should be ignored, since "gold standard" is just a common phrase
keywords["standard"] = 0
keywords["trump"] = 0
keywords["election"] = 0

# load the url_done.txt and remove any of the links that have been done before
with open('url_done.txt') as f:
    url_done = f.read().splitlines()

for idx, val in enumerate(gold["link"]):
    if val in url_done:
        gold["link"].remove(val)

temp_number = len(gold["link"])
print("after checking with url_done:", temp_number)
with open("log.txt", "a") as f:
    f.write(f"after checking with url_done: {temp_number} \n")

newly_added = 0
processed_links = []
# download the article, do NLP, get summary and keywords. write in file.
for url in gold["link"]:
    # print something at the beginning to better seperate the articles
    print(" ")
    print("----------------------------------------------------------------------------------------------------------------")
    # sleep between downloads, otherwise server thinks its an DoS attack due to the many get requests
    time.sleep(1.0)
    article = Article(url)
    try:
        article.download()
        article.parse()
    except:
        print("could not download or parse", url)
        continue
    # check datetime of the article. Dont save articles that are more than 1 day old.
    publish_time = article.publish_date
    print(publish_time)
    if publish_time != None:
        if publish_time.strftime('%Y-%m-%d') != today.strftime('%Y-%m-%d') and publish_time.strftime('%Y-%m-%d') != yesterday.strftime('%Y-%m-%d'):
            print("not up to date. Skipped")
            continue
    # as long as I get to download and parse the article, I successfully processed the link. Faults beyond this point wont change the outcome when rerun.
    processed_links.append(url)
    article.nlp()
    # check if the article has keywords associated with the top 20 keywords related to the subject. Only write if true
    # sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]      #will return both the key and value
    # if any(e in sorted(keywords, key=keywords.get, reverse=True)[:10] for e in article.keywords):
    # requires at least 2 keywords. Seems to work better, as "gold" alone is insufficient
    if sum([1 for e in article.keywords if e in sorted(keywords, key=keywords.get, reverse=True)[:50]]) >= 3:
        pass
    else:
        print("Keywords are not significant", url)
        print(article.keywords)
        continue
    # get file name based on the items in the folder
    if not os.listdir('to_classify'):
        # if folder is empty
        name = 0
    else:
        # for every item in the folder -> extract the digits using re.search -> convert the result to int and append using list comprehension -> find max
        name = max([int(re.search(r"([\d]+)", i).group(0))
                    for i in os.listdir('to_classify')]) + 1

    # write the article summary in a text file and save in folder using the naming scheme above. The try and except are used to prevent loop stopping due to weird article summary.
    try:
        text_file = open(f"to_classify/{name}.txt", "w")
        text_file.write("%s\n %s" % (publish_time, article.summary))
        text_file.close()
        # save the text for cross-validification of the summary
        text_file = open(f"to_classify/full{name}.txt", "w")
        text_file.write("%s\n %s" % (publish_time, article.text))
        text_file.close()
    except:
        print("could not write", url)
        continue
    newly_added += 1

print(" ")
print("++++++++++++++++++++++-----------------SUMMARY-----------------++++++++++++++++++++++++++++++++++")
# update the keywords with every iteration/article
for i in article.keywords:
    if i in keywords:
        keywords[i] += 1
    else:
        keywords[i] = 1
print("newly added:", newly_added)
with open("log.txt", "a") as f:
    f.write(f"newly added: {newly_added} \n")

# save the updated keywords after all articles have been done
np.save('keywords.npy', keywords)

# update the url_done text by appending all the new urls that have been processed.
with open("url_done.txt", "a") as f:
    for i in processed_links:
        f.write(i + "\n")
