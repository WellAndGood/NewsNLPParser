import numpy as np
import pprint
import datetime
import spacy
from AP_article_builder import AP_article_dict_builder, AP_article_full_txt
from spacy_methods import (
    get_specific_entities,
    entity_counter,
    append_to_array,
    entity_indexer,
    sentence_generator,
    verb_matcher,
    verb_in_sentence,
)
import sqlite3
import re
from prettytable import PrettyTable
from datetime import datetime
import hashlib


def table_delete(table_name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Table creation - Unique article reference table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    print(f"{table_name} table deleted")

    conn.commit()
    conn.close()


# table_delete("ARTICLES_REFERENCE")
# table_delete("VERBS_REFERENCE")
table_delete("ENTITIES_REFERENCE")
