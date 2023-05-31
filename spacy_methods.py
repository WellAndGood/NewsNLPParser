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
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_md")

# https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01

# Base URL, and use
url = "https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01"
article_dict = AP_article_dict_builder(url)
article_txt = AP_article_full_txt(url)

# Initialize the Doc object
doc = nlp(article_txt)

# Generate list of sentences from Doc object
def sentence_generator(txt):
    doc = nlp(txt)
    sentences = [sent.text for sent in doc.sents]
    return list(sentences)


sentences = sentence_generator(doc)

# Retrieve and store entities


def get_specific_entities(sentences):
    specific_entities = []
    sentence_count = -1
    previous_sentence = None

    word_count = 0

    for i, sent in enumerate(sentences):
        sentence_count += 1
        doc = nlp(sent)

        for j, ent in enumerate(doc.ents):
            if ent.text in sent:
                if ent.label_ in ["GPE", "ORG", "PERSON"]:
                    start_index = ent.start  # Start index of the entity
                    end_index = ent.end - 1  # End index of the entity
                    sentence = ent.sent.text  # The text of the sentence
                    sentence_start = (
                        ent.sent.start
                    )  # Index of the first word in the sentence
                    sentence_end = (
                        ent.sent.end - 1
                    )  # Index of the last word in the sentence
                    sentence_index = ent.start - sentence_start
                    word_index = word_count + start_index

                    specific_entities.append(
                        [
                            ent.text,
                            ent.label_,
                            start_index,
                            end_index,
                            sentence,
                            sentence_count,
                            sentence_start,
                            sentence_end,
                            word_index,
                        ]
                    )

            # Adds the sentence_end indexing to the total word count
        word_count += len(doc)
    return specific_entities


entities = get_specific_entities(sentences)

# raw_entity_list = list(entities)

# Counts the number of distinct times an entity appears in the article.
def entity_counter(lst):

    raw_entity_list = list(entities)
    count_dict = {}

    # Index the list elements to a dictionary and increment their counts
    for i, item in enumerate(lst):

        entity_sentence_check = "{}".format(item[0])
        if entity_sentence_check in count_dict:
            count_dict[entity_sentence_check] += 1
        else:
            count_dict[entity_sentence_check] = 1
    return count_dict


duplicate_items = entity_counter(entities)

# Algorithm to assign new key values to 1, increment if already existing
def append_to_array(key, value, dict_to_check):
    if key in dict_to_check:
        dict_to_check[key].append(value)
    else:
        dict_to_check[key] = [value]


raw_entity_list = list(entities)


def entity_indexer(lst):
    ent_index_dict = {}

    for i, entity_item in enumerate(lst):
        entity_sentence_check = "{}".format(entity_item[0])

        # entity_item[0] - Entity's name as a string
        # entity_item[5] - the sentence number index

        append_to_array(entity_item[0], entity_item[5], ent_index_dict)
    return ent_index_dict


ent_sentence_index = entity_indexer(raw_entity_list)


def verb_matcher(txt):
    # Verb Finder with Matcher
    verb_matcher = Matcher(nlp.vocab)
    verb_pattern = [{"POS": "VERB", "OP": "+"}]
    verb_matcher.add("VERBS", [verb_pattern])
    matches = verb_matcher(txt)

    verb_information = []

    for match in matches:

        word_index = match[1]
        original_verb = doc[match[1]]
        lemmatized_verb = doc[match[1]].lemma_
        verb_information.append([word_index, original_verb, lemmatized_verb])

    return verb_information


verbs = verb_matcher(doc)
# print(verbs)

# List of Verbs
verbs = verb_matcher(doc)

# List of Article's Sentences

sentences = sentence_generator(doc)


def verb_in_sentence(list_of_verbs, list_of_sentences):
    # print(list_of_sentences)

    nlp = spacy.load("en_core_web_md")
    specific_verbs = []
    sentence_count = -1
    previous_sentence = None

    word_count = 0

    for i, sent in enumerate(list_of_sentences):
        sentence_count += 1

        # Check the sentence's text matches the previous sentence's
        try:
            doc = nlp(sent)
            # print(doc)
            sentence = doc.text

            for token in doc:
                word_count += 1
                if token.pos_ == "VERB":

                    # verb_index = word_count + token.i
                    verb_text = token.text
                    verb_lemma = token.lemma_
                    sent_word_index = (
                        token.i
                    )  # Start index of the verb relative to the sentence

                    # Document
                    specific_verbs.append(
                        (
                            verb_text,
                            verb_lemma,
                            word_count,
                            sentence,
                            sentence_count,
                            sent_word_index,
                        )
                    )
        except:
            continue

    return specific_verbs


the_verbs = verb_in_sentence(verbs, sentences)
ppv = pprint.PrettyPrinter(indent=4)
# ppv.pprint(the_verbs)
