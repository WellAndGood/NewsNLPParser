import argparse
import spacy
from AP_article_builder import AP_article_dict_builder, AP_article_full_txt
from spacy_methods import get_specific_entities, entity_counter, append_to_array, entity_indexer, sentence_generator, verb_matcher, verb_in_sentence

parser = argparse.ArgumentParser()
parser.add_argument("URL", help="URL to process")
args = parser.parse_args()


nlp = spacy.load("en_core_web_md")

# Base URL. Use to obtain article information
url = args.URL
article_dict = AP_article_dict_builder(url)
article_txt = AP_article_full_txt(url)

# Initialize the Doc object
doc = nlp(article_txt)

sentences = sentence_generator(doc)
verbs = verb_matcher(doc)


if __name__ == "__main__":
    print(url)
    print(typeofv)