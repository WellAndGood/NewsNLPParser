import sqlite3
from typing import Dict, List, Union, AnyStr

def table_delete(table_name: str) -> AnyStr:
    conn = sqlite3.connect("NLPdatabase.db")
    cursor = conn.cursor()

    # Table creation - Unique article reference table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    print(f"{table_name} table deleted")

    conn.commit()
    conn.close()


# table_delete("ARTICLES_REFERENCE")
# table_delete("VERBS_REFERENCE")
# table_delete("ENTITIES_REFERENCE")


def null_id_delete() :
    conn = sqlite3.connect("db/NLPdatabase.db")
    cursor = conn.cursor()

    # Table creation - Unique article reference table
    cursor.execute("DELETE FROM ARTICLES_REFERENCE WHERE search_id IS NULL")

    conn.commit()
    conn.close()

null_id_delete()