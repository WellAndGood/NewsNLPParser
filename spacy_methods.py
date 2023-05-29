
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
from AP_article_builder import AP_article_dict_builder, AP_article_full_txt

nlp = spacy.load("en_core_web_md")

# https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01

# Base URL, and use
url = "https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01"
article_dict = AP_article_dict_builder(url)
article_txt = AP_article_full_txt(url)

# Initialize the Doc object
doc = nlp(article_txt)

# Generate list of sentences from Doc object
sentences = [sent.text for sent in doc.sents]

# Retrieve and store entities

def get_specific_entities(sentences):
    specific_entities = []
    sentence_count = -1
    previous_sentence = None
    
    for i, sent in enumerate(sentences):
        sentence_count += 1
        
        doc = nlp(sent)
        
        for j, ent in enumerate(doc.ents):
            if ent.text in sent:
                if ent.label_ in ["GPE", "ORG", "PERSON"]:
                    start_index = ent.start          # Start index of the entity
                    end_index = ent.end - 1          # End index of the entity
                    sentence = ent.sent.text         # The text of the sentence 
                    sentence_start = ent.sent.start  # Index of the first word in the sentence
                    sentence_end = ent.sent.end - 1  # Index of the last word in the sentence
                    sentence_index = ent.start - sentence_start 
                    # print("ent.start:", ent.start)
                    # print("sentence_start:", sentence_start)
                    # print("sentence_index:", sentence_index)

                    specific_entities.append((ent.text, ent.label_, start_index, end_index, sentence, sentence_count, sentence_start, sentence_end))
    return specific_entities

entities = get_specific_entities(sentences)

for entity in entities:
   print(entity[0], entity[1], entity[2], entity[3], entity[4], entity[5], entity[6], entity[7])
   print("")
   print("")






