import sqlite3


def article_reference_table_delete():
    conn = sqlite3.connect("NLPdatabase.db")
    cursor = conn.cursor()

    # Table creation - Unique article reference table
    # cursor.execute(f"DROP TABLE IF EXISTS ARTICLES_REFERENCE")
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS ARTICLES_REFERENCE (
                    id INTEGER PRIMARY KEY,     
                    art_id_hash TEXT,      
                    art_headline TEXT,       
                    sentence_id INTEGER, 
                    sentence_contents TEXT,     
                    authors TEXT,       
                    source_url TEXT,        
                    published_time TEXT,
                    modified_time TEXT)
        """
    )

    conn.commit()
    conn.close()

def verbs_reference_table_create():

    conn = sqlite3.connect("NLPdatabase.db")
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
    conn.commit()
    conn.close()

def entity_reference_table_insert():

    conn = sqlite3.connect("NLPdatabase.db")
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
    conn.commit()
    conn.close()


article_reference_table_delete()
verbs_reference_table_create()
entity_reference_table_insert()