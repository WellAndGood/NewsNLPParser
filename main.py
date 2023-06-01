import argparse
import spacy
from AP_article_builder import ap_article_dict_builder, ap_article_full_txt
from spacy_methods import (
    sentence_generator,
    verb_matcher,
)

parser = argparse.ArgumentParser()
parser.add_argument("URL", help="URL to process")
args = parser.parse_args()


nlp = spacy.load("en_core_web_md")

# Base URL. Use to obtain article information
url = args.URL
article_dict = ap_article_dict_builder(url)
article_txt = ap_article_full_txt(url)

# Initialize the Doc object
doc = nlp(article_txt)

sentences = sentence_generator(doc)
verbs = verb_matcher(doc)


if __name__ == "__main__":
    print(url)
