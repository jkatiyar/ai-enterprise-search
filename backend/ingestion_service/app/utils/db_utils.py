import psycopg
from app.core.db_config import DB_CONFIG


def get_db_connection():
    return psycopg.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )


def insert_document_metadata(filename, file_path, text_length, num_chunks):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO documents (filename, file_path, text_length, num_chunks)
        VALUES (%s, %s, %s, %s)
        """,
        (filename, file_path, text_length, num_chunks),
    )

    conn.commit()
    cur.close()
    conn.close()
