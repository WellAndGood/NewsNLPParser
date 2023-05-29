import numpy as np
import pprint
import datetime
from AP_article_builder import AP_article_dict_builder, AP_article_full_txt
from spacy_methods import get_specific_entities, entity_counter, append_to_array, entity_indexer
import sqlite3
import re
from prettytable import PrettyTable
import hashlib


article_dict = AP_article_dict_builder("https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01")

def hash_string(string):
    hash_object = hashlib.md5()
    hash_object.update(string.encode())
    return hash_object.hexdigest()

art_headline = article_dict["headline"]
hashed_string = hash_string(art_headline)
print(hashed_string)


