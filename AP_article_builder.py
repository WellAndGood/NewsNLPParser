import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pprint
import csv
import datetime
import nltk
import requests
import csv
import json
import spacy
from spacy import displacy
import pprint

# Works for Associated Press Articles
def AP_article_dict_builder(url):

    # Takes URL, outputs Beautiful Soup html
    response = requests.get(url)
    APArticle = BeautifulSoup(response.content, 'html.parser')

    article_information = {}

    # Retrieves canonical link
    canonical_links = APArticle.find_all('link', rel='canonical')

    # Print the href attribute of each matching link
    for link in canonical_links:
        self_URL = link.get('href')
        
    article_information["self_URL"] = self_URL

    # Retrieves article headline
    main_Headline = APArticle.find_all('h1')
    main_Headline = main_Headline[0].text
    article_information["headline"] = main_Headline

    # Retrieves article datetime metadata
    published_time = APArticle.find('meta', {'property': 'article:published_time'}).get('content')
    modified_time = APArticle.find('meta', {'property': 'article:modified_time'}).get('content')
    article_information["published_time"] = published_time
    article_information["modified_time"] = modified_time
    
    # Retrieves authors
    author_list = []
    scripts = APArticle.find('script', attrs={'data-rh': 'true', 'type': 'application/ld+json'})
    JSONscript = json.loads(scripts.text)
    author_list = JSONscript['author']
    article_information["author(s)"] = author_list

    # Retrieves image data
    image_data = []
    image_url = JSONscript['image']
    image_caption_div = APArticle.find_all('div', attrs={'data-key': 'embed-caption'})
    image_caption = image_caption_div[0].text
    try: 
        image_attribution = image_caption[-50:].replace(")", "").split("(")[1]
    except:
        image_attribution = ""

    image_data.append([image_url, image_caption, image_attribution])
    
    # Retrieves paragraph data
    paragraphCount = 0
    article_paragraphs = []

    article_content = APArticle.find_all('div', {'class': 'Article', 'data-key': 'article'})
    inner_para = article_content[0].find_all('p')

    # Loops through the paragraphs to find inner information
    for index, para in enumerate(inner_para):
        
        paragraphCount += 1
        inner_text = para.text 
        inner_links = para.find_all('a')
        content, href = "", ""
        
        # reset the array
        inner_link = []

        # Traverse the list to retrieve links and its associated text    
        for link in inner_links:
            content = link.string.strip()
            href = link['href']
            if href[0] == "/":
                href = "https://apnews.com" + href 
            inner_link.append([content, href])
            para_ele = para.name
        article_paragraphs.append([index, inner_text, inner_link])

    article_information["mainContents"] = article_paragraphs

    return article_information


# https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01

def AP_article_full_txt(url):
    article_dict = AP_article_dict_builder(url)
    paragraph_contents = article_dict["mainContents"]

    entire_article = ""

    for i, content in enumerate(paragraph_contents):
        entire_article += f" {content[1]}"
    
    return entire_article


#AP_article_full_txt("https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01")

