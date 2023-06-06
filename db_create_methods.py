import sqlite3


def article_reference_table_create():
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
                    modified_time TEXT
                );
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
                );"""
    )
    conn.commit()
    conn.close()

def entity_reference_table_create():

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
            );"""
    )
    conn.commit()
    conn.close()

def search_reference_table_create():

    conn = sqlite3.connect("NLPdatabase.db")
    cursor = conn.cursor()

    # Table creation - Entities
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS SEARCHES_REFERENCE (
                id INTEGER PRIMARY KEY,
                url TEXT,
                title TEXT DEFAULT 'Untitled',
                search_datetime DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
    )
    conn.commit()
    conn.close()


def alter_table():
    conn = sqlite3.connect("NLPdatabase.db")
    cursor = conn.cursor()

    # Table creation - Entities
    cursor.execute("""
        CREATE TABLE temp_SEARCHES_REFERENCE (
            id INTEGER PRIMARY KEY,
            url TEXT,
            title TEXT DEFAULT 'None - Analyze',
            search_datetime DATETIME DEFAULT CURRENT_TIMESTAMP
        ) 
    """)

    cursor.execute(""" INSERT INTO temp_SEARCHES_REFERENCE (id, url, title, search_datetime)
            SELECT id, url, title, search_datetime
            FROM SEARCHES_REFERENCE """)
    
    cursor.execute(""" DROP TABLE SEARCHES_REFERENCE """ )

    cursor.execute(""" ALTER TABLE temp_SEARCHES_REFERENCE RENAME TO SEARCHES_REFERENCE """ )

    conn.commit()
    conn.close()

# alter_table()


article_reference_table_create()
verbs_reference_table_create()
entity_reference_table_create()
search_reference_table_create()