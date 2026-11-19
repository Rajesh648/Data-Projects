import psycopg2
from psycopg2.extensions import register_adapter, AsIs
import numpy as np

# NUMPY ARRAY SUPPORT
register_adapter(np.ndarray, lambda arr: AsIs(list(arr)))


# DATABASE CONNECTION
def get_connection():

    return psycopg2.connect(
        host="localhost",
        database="face_db",
        user="postgres",
        password="rajesh815"
    )


# GET ALL PERSONS
def get_all_persons():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            age,
            gender,
            phone,
            address,
            email,
            occupation,
            image_path,
            embedding
        FROM persons
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


# UPDATE FACE EMBEDDING
def update_embedding(person_id, embedding):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE persons
        SET embedding = %s
        WHERE id = %s
        """,
        (embedding.tolist(), person_id)
    )

    conn.commit()

    cur.close()
    conn.close()