import datetime
import spacy
from AP_article_builder import ap_article_dict_builder, ap_article_full_txt
from spacy_methods import (
    get_specific_entities,
    sentence_generator,
    verb_matcher,
    verb_in_sentence,
)
import sqlite3
import re
from datetime import datetime
import hashlib
from typing import Optional

"""
DATA ACCESS LAYER
# Prepares variables obtained through the dict_builder for the SQLite table

Author(s):
May 29, 2023 - Daniel Pisani - Initial creation of this file
"""

# Creates a unique hash of a string
def hash_string(string: str) -> Optional[str]:
    hash_object = hashlib.md5()
    hash_object.update(string.encode())
    return hash_object.hexdigest()


# Sentence list
url = "https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01"
article_txt = ap_article_full_txt(url)
nlp = spacy.load("en_core_web_md")
doc = nlp(article_txt)
sentences = sentence_generator(doc)
verbs = verb_matcher(doc)

# Creates a unique hash for the article's headline
article_dict = ap_article_dict_builder(
    "https://apnews.com/article/george-santos-federal-charges-updates-33667a0900271e5002459ab748d8fdc8?utm_source=homepage&utm_medium=TopNews&utm_campaign=position_01"
)
art_headline = article_dict["headline"]
hashed_string = hash_string(art_headline)

# Provide unique article name for the table's name
art_headline = article_dict["headline"]
unique_article_name = article_dict["headline"].replace(" ", "").lower()
unique_article_name = re.sub(r"\W+", "", unique_article_name)[:100]

# Create hash for articleID - hash_string is a created function
# (Would detect change in title wording)
art_id_hash = hash_string(art_headline)

# Author
list_author = article_dict["author(s)"]
art_author = ",".join(list_author)

# Source (URL)
source_url = article_dict["self_URL"]

# Published time
published_time = article_dict["published_time"]

# Modified time
modified_time = article_dict["modified_time"]


def article_reference_table_insert(sent_list: list) -> None:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Table creation - Unique article reference table
    # cursor.execute(f"DROP TABLE IF EXISTS ARTICLES_REFERENCE")
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS ARTICLES_REFERENCE (
                    id INTEGER PRIMARY KEY,     art_id_hash TEXT,      art_headline TEXT,       sentence_id INTEGER, 
                    sentence_contents TEXT,     authors TEXT,       source_url TEXT,        published_time TEXT,
                    modified_time TEXT)"""
    )

    cursor.execute(
        "SELECT COUNT(*) FROM ARTICLES_REFERENCE WHERE art_id_hash = ? ", (art_id_hash,)
    )
    result = cursor.fetchone()
    print(result)
    print(result[0])

    modified_time = article_dict["modified_time"]
    # modified_time = "2023-05-12T02:56:06Z"

    if result[0] == 0:
        print("There is nothing in the table")
        # The hash does not exist in our table, meaning that
        # a) there is no matching article title, and
        # b) we may freely INSERT this information

        # INSERTing each sentence into the ref. table
        for i, element in enumerate(sent_list):
            cursor.execute(
                f"""INSERT INTO ARTICLES_REFERENCE (
                            art_headline,       art_id_hash,        sentence_id,        sentence_contents, 
                            authors,        source_url,         published_time,         modified_time) 
                        VALUES ('{art_headline}', '{art_id_hash}', {i}, '{element}', 
                                '{art_author}', '{source_url}', '{published_time}', '{modified_time}')"""
            )
    else:
        cursor.execute(
            "SELECT * FROM ARTICLES_REFERENCE WHERE art_id_hash = ? ORDER BY modified_time DESC",
            (art_id_hash,),
        )
        results = cursor.fetchall()

        # If there are results
        if results:
            latest_modified_db_time = results[0][8]
            print(latest_modified_db_time)

            # If the article's modified_time (the one being parsed) is more recent than the latest database time
            if modified_time > latest_modified_db_time:
                for i, element in enumerate(sent_list):
                    cursor.execute(
                        f"""INSERT INTO ARTICLES_REFERENCE (
                                    art_headline,       art_id_hash,        sentence_id,        sentence_contents, 
                                    authors,        source_url,         published_time,         modified_time) 
                                VALUES ('{art_headline}', '{art_id_hash}', {i}, '{element}', 
                                        '{art_author}', '{source_url}', '{published_time}', '{modified_time}')"""
                    )

            # If there is a more recent DB entry, the article does not get submitted (What's the point?)
            else:
                print(f"{modified_time} does not {latest_modified_db_time}")

    conn.commit()
    conn.close()


article_reference_table_insert(sentences)


def verbs_reference_table_insert(verbs_list: list) -> None:

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Table creation - Verbs
    # cursor.execute(f"DROP TABLE IF EXISTS VERBS_REFERENCE")
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS VERBS_REFERENCE (
                    id INTEGER PRIMARY KEY, 
                    art_id_hash TEXT REFERENCES ARTICLES_REFERENCE (art_id_hash) , 
                    art_headline TEXT,
                    verb_text TEXT,
                    lemmatized_text TEXT,
                    article_word_index INTEGER,
                    sentence_id INTEGER,
                    sent_word_index INTEGER,
                    timestamp TEXT,
                    modified_time TEXT
                    )"""
    )

    cursor.execute(
        "SELECT COUNT(*) FROM VERBS_REFERENCE WHERE art_id_hash = ? ", (art_id_hash,)
    )
    result = cursor.fetchone()
    print(result)
    print(result[0])

    # modified_time = article_dict["modified_time"]
    modified_time = "2023-05-13T02:56:06Z"

    # If there is no count == no entries already existing in the table
    if result[0] == 0:
        print("There is nothing in the table")

        # INSERTing each sentence into the ref. table
        for i, element in enumerate(verbs_list):
            verb_text = element[0]
            lemmatized_text = element[1]
            article_word_index = element[2]
            sentence_id = element[4]
            sent_word_index = element[5]
            timestamp = datetime.now()

            cursor.execute(
                f"""INSERT INTO VERBS_REFERENCE (
                            art_id_hash,
                            art_headline,
                            verb_text,
                            lemmatized_text,
                            article_word_index,
                            sentence_id,
                            sent_word_index,
                            timestamp,
                            modified_time    
                            ) 
                        VALUES ('{art_id_hash}', '{art_headline}', '{verb_text}', '{lemmatized_text}', 
                                '{article_word_index}', '{sentence_id}', {sent_word_index}, '{timestamp}', 
                                '{modified_time}'
                                )
                        """
            )

        else:
            cursor.execute(
                "SELECT * FROM VERBS_REFERENCE WHERE art_id_hash = ? ORDER BY modified_time DESC",
                (art_id_hash,),
            )
            results = cursor.fetchall()

            if results:
                latest_modified_db_time = results[0][9]
                print(latest_modified_db_time)

                if modified_time > latest_modified_db_time:
                    for i, element in enumerate(verbs_list):
                        cursor.execute(
                            f"""INSERT INTO VERBS_REFERENCE (
                            art_id_hash,
                            art_headline,
                            verb_text,
                            lemmatized_text,
                            article_word_index,
                            sentence_id,
                            sent_word_index,
                            timestamp,
                            modified_time    
                            ) 
                        VALUES ('{art_id_hash}', '{art_headline}', '{verb_text}', '{lemmatized_text}', 
                                '{article_word_index}', '{sentence_id}', {sent_word_index}, '{timestamp}', 
                                '{modified_time}'
                                )
                        """
                        )
                else:
                    print(f"{modified_time} does not surpass {latest_modified_db_time}")

    conn.commit()
    conn.close()


the_verbs = verb_in_sentence(verbs, sentences)
verbs_reference_table_insert(the_verbs)


def entity_reference_table_insert(entity_list: list) -> None:

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Table creation - Entities
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS ENTITIES_REFERENCE (
                id INTEGER PRIMARY KEY, 
                art_id_hash TEXT REFERENCES ENTITIES_REFERENCE (art_id_hash), 
                art_headline TEXT,
                entity_text TEXT,
                entity_type TEXT,
                word_index_start INTEGER,
                word_index_end INTEGER,
                sentence_id INTEGER,
                timestamp TEXT,
                modified_time TEXT
                )"""
    )

    cursor.execute(
        "SELECT COUNT(*) FROM ENTITIES_REFERENCE WHERE art_id_hash = ? ", (art_id_hash,)
    )
    result = cursor.fetchone()
    print(result)
    print(result[0])

    modified_time = article_dict["modified_time"]
    # modified_time = "2023-05-14T02:56:06Z"

    # If there is no count == no entries already existing in the table
    if result[0] == 0:
        print("There is nothing in the table")

        # INSERTing each sentence into the ref. table
        for i, entity in enumerate(entity_list):

            entity_text = entity[0]
            entity_type = entity[1]
            word_index_start = entity[2]
            word_index_end = entity[3]
            sentence_id = entity[5]
            timestamp = datetime.now()

            cursor.execute(
                f"""INSERT INTO ENTITIES_REFERENCE (
                            art_id_hash,
                            art_headline,
                            entity_text,
                            entity_type,
                            word_index_start,
                            word_index_end,
                            sentence_id,
                            timestamp,
                            modified_time
                            ) 
                        VALUES ('{art_id_hash}', '{art_headline}', '{entity_text}', '{entity_type}', 
                        '{word_index_start}', '{word_index_end}', '{sentence_id}', '{timestamp}', '{modified_time}')
                        """
            )
    else:
        cursor.execute(
            "SELECT * FROM VERBS_REFERENCE WHERE art_id_hash = ? ORDER BY modified_time DESC",
            (art_id_hash,),
        )
        results = cursor.fetchall()

        if results:
            latest_modified_db_time = results[0][9]
            print(latest_modified_db_time)

            if modified_time > latest_modified_db_time:
                for i, entity in enumerate(entity_list):
                    entity_text = entity[0]
                    entity_type = entity[1]
                    word_index_start = entity[2]
                    word_index_end = entity[3]
                    sentence_id = entity[5]
                    timestamp = datetime.now()
                    cursor.execute(
                        f"""INSERT INTO ENTITIES_REFERENCE (
                            art_id_hash,
                            art_headline,
                            entity_text,
                            entity_type,
                            word_index_start,
                            word_index_end,
                            sentence_id,
                            timestamp,
                            modified_time
                            ) 
                        VALUES ('{art_id_hash}', '{art_headline}', '{entity_text}', '{entity_type}', 
                        '{word_index_start}', '{word_index_end}', '{sentence_id}', '{timestamp}', '{modified_time}')
                        """
                    )
            else:
                print(f"{modified_time} does not surpass {latest_modified_db_time}")

    conn.commit()
    conn.close()

raw_entity_list = get_specific_entities(sentences)
entity_reference_table_insert(raw_entity_list)
