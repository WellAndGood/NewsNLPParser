import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pprint
import datetime
import nltk
import requests
import csv
import json
import spacy
from spacy import displacy
from AP_article_builder import AP_article_dict_builder, AP_article_full_txt
from spacy_methods import (
    get_specific_entities,
    entity_counter,
    append_to_array,
    entity_indexer,
)


def parse_sentences(text):
    sentences = list(doc.sents)
    return sentences
