import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()  # Loading environment variables from .env file

@contextmanager
def get_db_connection():
    """Context manager for database connection."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        yield conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise
    finally:
        if conn:
            conn.close()