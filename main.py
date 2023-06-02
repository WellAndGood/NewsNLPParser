import argparse
import spacy
from AP_article_builder import ap_article_dict_builder, ap_article_full_txt
from spacy_methods import (
    sentence_generator,
    get_specific_entities,
    entity_counter,
    verb_in_sentence,
    verb_matcher,
)
from db_interaction import (article_reference_table_insert, 
    verbs_reference_table_insert, 
    entity_reference_table_insert
)

parser = argparse.ArgumentParser()
parser.add_argument("URL", help="URL to process")
args = parser.parse_args()


if __name__ == "__main__":

    nlp = spacy.load("en_core_web_md")

    # Base URL. Use to obtain article information
    url = args.URL
    article_dict = ap_article_dict_builder(url)
    article_txt = ap_article_full_txt(url)

    # Initialize the Doc object, generate sentences, verbs, entities, from the article
    doc = nlp(article_txt)
    sentences = sentence_generator(doc)
    verbs = verb_matcher(doc)
    entities = get_specific_entities(sentences)
    raw_entity_list = list(entities)
    duplicate_items = entity_counter(entities)
    the_verbs = verb_in_sentence(verbs, sentences)

    # Insert article information into their distinct tables
    article_reference_table_insert(sentences)
    verbs_reference_table_insert(the_verbs)
    entity_reference_table_insert(raw_entity_list)
