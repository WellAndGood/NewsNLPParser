import spacy
from spacy.tokens import Doc
from srs.AP_article_builder import ap_article_dict_builder, ap_article_full_txt
from spacy.matcher import Matcher
from typing import Dict, List, Union

nlp = spacy.load("en_core_web_md")

# Temporary stand-in URL
url = "https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01"
article_dict = ap_article_dict_builder(url)
article_txt = ap_article_full_txt(url)

# Initialize the Doc object
doc = nlp(url)

# Generate list of sentences from Doc object
def sentence_generator(txt: str) -> List[str]:
    doc = nlp(txt)
    sentences = [sent.text for sent in doc.sents]
    return list(sentences)

sentences = sentence_generator(doc)

# Retrieve and store entities
def get_specific_entities(sentences: list) -> List[Union[str, int]]:
    specific_entities = []
    sentence_count = -1

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

# Counts the number of distinct times an entity appears in the article.
def entity_counter(lst) -> Dict[str, int]:

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
def append_to_array(key: str, value: int, dict_to_check: dict) -> None:
    if key in dict_to_check:
        dict_to_check[key].append(value)
    else:
        dict_to_check[key] = [value]


raw_entity_list = list(entities)

def entity_indexer(lst: list) -> Dict[str, List[int]]:
    ent_index_dict = {}

    for i, entity_item in enumerate(lst):
        entity_sentence_check = "{}".format(entity_item[0])

        ### entity_item[0] - Entity's name as a string
        ### entity_item[5] - the sentence number index

        append_to_array(entity_item[0], entity_item[5], ent_index_dict)
    return ent_index_dict


def verb_matcher(doc: Doc) -> List[Union[int, str]]:
    # Verb Finder with Matcher
    verb_matcher = Matcher(nlp.vocab)
    verb_pattern = [{"POS": "VERB", "OP": "+"}]
    verb_matcher.add("VERBS", [verb_pattern])
    matches = verb_matcher(doc)

    verb_information = []

    for match in matches:
        word_index = match[1]
        original_verb = doc[match[1]]
        lemmatized_verb = doc[match[1]].lemma_
        verb_information.append([word_index, original_verb, lemmatized_verb])

    return verb_information

# List of Verbs
verbs = verb_matcher(doc)

# List of Article's Sentences
sentences = sentence_generator(doc)


def verb_in_sentence(list_of_verbs: list, list_of_sentences: list, doc: Doc) -> List[Union[str, int]]:

    nlp = spacy.load("en_core_web_md")
    specific_verbs = []
    sentence_count = -1
    word_count = 0

    for i, sent in enumerate(list_of_sentences):
        sentence_count += 1

        # Check the sentence's text matches the previous sentence's
        try:
            doc = nlp(sent)
            sentence = doc.text

            for token in doc:
                word_count += 1
                if token.pos_ == "VERB":
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

